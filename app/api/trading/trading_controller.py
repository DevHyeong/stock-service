from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional

from app.db import get_db
from app.repositories.trading_repository import TradingRepository
from app.services.trading_service import TradingService
from app.schemas.response import APIResponse
from app.schemas.trading import TradingSyncRequest
from app.domain.rank.services.rank_service import RankService
from app.domain.rank.enums.market_type import MarketType
from app.domain.rank.enums.mang_stk_incls import MangStkIncls

# Direct imports for dependency injection
from app.domain.rank.repositories.rank_repository import RankRepository
from app.domain.rank.rank_client import RankClient
from app.common.auth_client import AuthClient


router = APIRouter(prefix="/trading", tags=["거래 정보"])


def get_trading_service(
    db: AsyncSession = Depends(get_db)
) -> TradingService:
    """TradingService 의존성 주입"""
    # 직접 rank_service 생성
    auth_client = AuthClient()
    rank_client = RankClient()
    rank_repository = RankRepository(auth_client, rank_client)
    rank_service = RankService(rank_repository)

    repo = TradingRepository(db)
    return TradingService(repo, rank_service)


@router.post("/ranking/sync")
async def sync_trading_data(
    trade_date: Optional[date] = Query(None, description="거래일자 (없으면 오늘)"),
    limit: int = Query(100, ge=1, le=500, description="상위 N개만 저장"),
    market_type: MarketType = Query(MarketType.ALL, description="시장 유형"),
    include_managed: MangStkIncls = Query(MangStkIncls.EXCLUDE, description="관리종목 포함 여부"),
    db: AsyncSession = Depends(get_db)
):
    """거래대금 순위 데이터 동기화

    키움 API에서 거래대금 순위를 가져와 DB에 저장합니다.

    Args:
        trade_date: 거래일자 (기본값: 오늘)
        limit: 상위 N개만 저장 (기본값: 100개)
        market_type: 시장 유형 (ALL, KOSPI, KOSDAQ 등)
        include_managed: 관리종목 포함 여부

    Returns:
        동기화 결과 (저장된 종목 수, 총 거래대금)
    """
    try:
        # Create dependencies directly
        auth_client = AuthClient()
        rank_client = RankClient()
        rank_repository = RankRepository(auth_client, rank_client)
        rank_service = RankService(rank_repository)

        trading_repo = TradingRepository(db)
        trading_service = TradingService(trading_repo, rank_service)

        result = await trading_service.sync_trading_data(
            trade_date=trade_date,
            limit=limit,
            market_type=market_type,
            include_managed=include_managed
        )

        return APIResponse(
            success=True,
            message=f"{result.trade_date} 거래대금 순위 동기화 완료: {result.synced_count}건",
            data=result.model_dump()
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(
            success=False,
            message="거래대금 순위 동기화 실패",
            error=str(e)
        )


@router.get("/ranking/latest")
async def get_latest_ranking(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=500, description="조회 개수"),
    trading_service: TradingService = Depends(get_trading_service)
):
    """최신 거래대금 순위 조회

    DB에 저장된 가장 최근 날짜의 거래대금 순위를 조회합니다.

    Args:
        skip: 페이지네이션 오프셋
        limit: 조회 개수

    Returns:
        최신 거래대금 순위 리스트
    """
    try:
        # 오늘 날짜로 조회
        today = date.today()
        result = await trading_service.get_ranking_by_date(
            trade_date=today,
            skip=skip,
            limit=limit
        )

        return APIResponse(
            success=True,
            message="최신 거래대금 순위 조회 성공",
            data=result.model_dump()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="최신 거래대금 순위 조회 실패",
            error=str(e)
        )


@router.get("/ranking/{trade_date}")
async def get_trading_ranking(
    trade_date: date,
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=500, description="조회 개수"),
    trading_service: TradingService = Depends(get_trading_service)
):
    """특정 날짜의 거래대금 순위 조회

    DB에 저장된 특정 날짜의 거래대금 순위를 조회합니다.

    Args:
        trade_date: 거래일자 (YYYY-MM-DD)
        skip: 페이지네이션 오프셋
        limit: 조회 개수

    Returns:
        거래대금 순위 리스트
    """
    try:
        result = await trading_service.get_ranking_by_date(
            trade_date=trade_date,
            skip=skip,
            limit=limit
        )

        return APIResponse(
            success=True,
            message=f"{trade_date} 거래대금 순위 조회 성공",
            data=result.model_dump()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="거래대금 순위 조회 실패",
            error=str(e)
        )


@router.get("/history/{stock_code}")
async def get_stock_trading_history(
    stock_code: str,
    start_date: Optional[date] = Query(None, description="시작일자 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="종료일자 (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(30, ge=1, le=365, description="조회 개수"),
    trading_service: TradingService = Depends(get_trading_service)
):
    """종목별 거래 히스토리 조회

    특정 종목의 일별 거래 히스토리를 조회합니다.

    Args:
        stock_code: 종목코드
        start_date: 시작일자
        end_date: 종료일자
        skip: 페이지네이션 오프셋
        limit: 조회 개수

    Returns:
        종목별 거래 히스토리
    """
    try:
        result = await trading_service.get_stock_history(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )

        if result.total_count == 0:
            return APIResponse(
                success=False,
                message=f"종목 거래 히스토리를 찾을 수 없습니다: {stock_code}",
                error="No data found"
            )

        return APIResponse(
            success=True,
            message=f"{stock_code} 거래 히스토리 조회 성공",
            data=result.model_dump()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="거래 히스토리 조회 실패",
            error=str(e)
        )
