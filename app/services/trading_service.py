from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

from app.repositories.trading_repository import TradingRepository
from app.domain.rank.services.rank_service import RankService
from app.domain.rank.enums.market_type import MarketType
from app.domain.rank.enums.mang_stk_incls import MangStkIncls
from app.domain.rank.enums.stex_type import StexType
from app.schemas.trading import (
    TradingSyncResponse,
    TradingRankingResponse,
    StockTradingHistoryResponse,
    StockTradingDailyResponse
)


class TradingService:
    """거래 정보 서비스"""

    def __init__(self, repo: TradingRepository, rank_service: RankService):
        self.repo = repo
        self.rank_service = rank_service

    async def sync_trading_data(
        self,
        trade_date: Optional[date] = None,
        limit: int = 100,
        market_type: MarketType = MarketType.ALL,
        include_managed: MangStkIncls = MangStkIncls.EXCLUDE
    ) -> TradingSyncResponse:
        """거래대금 순위 데이터를 키움 API에서 가져와 DB에 저장

        Args:
            trade_date: 거래일자 (None이면 오늘)
            limit: 상위 N개만 저장
            market_type: 시장 유형
            include_managed: 관리종목 포함 여부

        Returns:
            동기화 결과
        """
        if trade_date is None:
            trade_date = date.today()

        # 1. 키움 API에서 거래대금 순위 조회
        rank_response = await self.rank_service.get_top_trading_volume_stocks(
            mrkt_tp=market_type,
            mang_stk_incls=include_managed,
            stex_tp=StexType.KRX
        )

        # 2. 상위 N개만 추출
        top_items = rank_response.trde_prica_upper[:limit]

        if not top_items:
            return TradingSyncResponse(
                trade_date=trade_date,
                synced_count=0,
                total_trading_amount=0
            )

        # 3. DB 저장 형식으로 변환
        trading_data = []
        total_trading_amount = 0

        for item in top_items:
            # 문자열을 숫자로 변환
            try:
                current_price = Decimal(item.cur_prc) if item.cur_prc else None
                change_amount = Decimal(item.pred_pre) if item.pred_pre else None
                change_rate = Decimal(item.flu_rt) if item.flu_rt else None
                sell_bid = Decimal(item.sel_bid) if item.sel_bid else None
                buy_bid = Decimal(item.buy_bid) if item.buy_bid else None
                trading_amount = int(item.trde_prica) if item.trde_prica else 0
                trading_volume = int(item.now_trde_qty) if item.now_trde_qty else 0
                prev_trading_volume = int(item.pred_trde_qty) if item.pred_trde_qty else 0
                current_rank = int(item.now_rank) if item.now_rank else None
                previous_rank = int(item.pred_rank) if item.pred_rank else None

                total_trading_amount += trading_amount

                trading_data.append({
                    'stock_code': item.stk_cd,
                    'stock_name': item.stk_nm,
                    'trade_date': trade_date,
                    'current_price': current_price,
                    'change_amount': change_amount,
                    'change_rate': change_rate,
                    'trading_amount': trading_amount,
                    'trading_volume': trading_volume,
                    'previous_trading_volume': prev_trading_volume,
                    'sell_bid': sell_bid,
                    'buy_bid': buy_bid,
                    'current_rank': current_rank,
                    'previous_rank': previous_rank
                })
            except (ValueError, TypeError) as e:
                print(f"데이터 변환 오류 - 종목: {item.stk_nm}, 에러: {e}")
                continue

        # 4. DB에 일괄 저장/업데이트
        synced_count = await self.repo.bulk_upsert(trading_data)

        return TradingSyncResponse(
            trade_date=trade_date,
            synced_count=synced_count,
            total_trading_amount=total_trading_amount
        )

    async def get_ranking_by_date(
        self,
        trade_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> TradingRankingResponse:
        """특정 날짜의 거래대금 순위 조회

        Args:
            trade_date: 거래일자
            skip: 건너뛸 개수
            limit: 조회 개수

        Returns:
            순위 정보
        """
        rankings = await self.repo.get_ranking_by_date(trade_date, skip, limit)
        total = await self.repo.count_by_date(trade_date)

        ranking_responses = [
            StockTradingDailyResponse.model_validate(r) for r in rankings
        ]

        return TradingRankingResponse(
            trade_date=trade_date,
            rankings=ranking_responses,
            total_count=total
        )

    async def get_stock_history(
        self,
        stock_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 30
    ) -> StockTradingHistoryResponse:
        """특정 종목의 거래 히스토리 조회

        Args:
            stock_code: 종목코드
            start_date: 시작일자
            end_date: 종료일자
            skip: 건너뛸 개수
            limit: 조회 개수

        Returns:
            종목별 거래 히스토리
        """
        history = await self.repo.get_stock_history(
            stock_code, start_date, end_date, skip, limit
        )
        total = await self.repo.count_stock_history(
            stock_code, start_date, end_date
        )

        if not history:
            return StockTradingHistoryResponse(
                stock_code=stock_code,
                stock_name="",
                history=[],
                total_count=0
            )

        history_responses = [
            StockTradingDailyResponse.model_validate(h) for h in history
        ]

        return StockTradingHistoryResponse(
            stock_code=stock_code,
            stock_name=history[0].stock_name if history else "",
            history=history_responses,
            total_count=total
        )
