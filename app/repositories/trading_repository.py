from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from datetime import date
from typing import List, Optional

from app.models.stock_trading_daily import StockTradingDaily


class TradingRepository:
    """거래 정보 Repository"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_upsert(self, trading_data: List[dict]) -> int:
        """일별 거래 정보 일괄 저장/업데이트

        Args:
            trading_data: 거래 정보 리스트

        Returns:
            저장된 개수
        """
        if not trading_data:
            return 0

        stmt = insert(StockTradingDaily).values(trading_data)

        # ON DUPLICATE KEY UPDATE
        update_dict = {
            'stock_name': stmt.inserted.stock_name,
            'current_price': stmt.inserted.current_price,
            'change_amount': stmt.inserted.change_amount,
            'change_rate': stmt.inserted.change_rate,
            'trading_amount': stmt.inserted.trading_amount,
            'trading_volume': stmt.inserted.trading_volume,
            'previous_trading_volume': stmt.inserted.previous_trading_volume,
            'sell_bid': stmt.inserted.sell_bid,
            'buy_bid': stmt.inserted.buy_bid,
            'current_rank': stmt.inserted.current_rank,
            'previous_rank': stmt.inserted.previous_rank,
            'updated_at': func.now()
        }

        stmt = stmt.on_duplicate_key_update(**update_dict)

        result = await self.db.execute(stmt)
        await self.db.commit()

        return len(trading_data)

    async def get_by_date_and_code(self, trade_date: date, stock_code: str) -> Optional[StockTradingDaily]:
        """특정 날짜의 특정 종목 거래 정보 조회

        Args:
            trade_date: 거래일자
            stock_code: 종목코드

        Returns:
            거래 정보
        """
        stmt = select(StockTradingDaily).where(
            and_(
                StockTradingDaily.trade_date == trade_date,
                StockTradingDaily.stock_code == stock_code
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_ranking_by_date(
        self,
        trade_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[StockTradingDaily]:
        """특정 날짜의 거래대금 순위 조회

        Args:
            trade_date: 거래일자
            skip: 건너뛸 개수
            limit: 조회 개수

        Returns:
            거래 정보 리스트 (순위순)
        """
        stmt = select(StockTradingDaily).where(
            StockTradingDaily.trade_date == trade_date
        ).order_by(
            StockTradingDaily.current_rank.asc()
        ).offset(skip).limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def count_by_date(self, trade_date: date) -> int:
        """특정 날짜의 전체 개수 조회

        Args:
            trade_date: 거래일자

        Returns:
            전체 개수
        """
        stmt = select(func.count(StockTradingDaily.id)).where(
            StockTradingDaily.trade_date == trade_date
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_stock_history(
        self,
        stock_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 30
    ) -> List[StockTradingDaily]:
        """특정 종목의 거래 히스토리 조회

        Args:
            stock_code: 종목코드
            start_date: 시작일자
            end_date: 종료일자
            skip: 건너뛸 개수
            limit: 조회 개수

        Returns:
            거래 정보 리스트 (날짜 역순)
        """
        conditions = [StockTradingDaily.stock_code == stock_code]

        if start_date:
            conditions.append(StockTradingDaily.trade_date >= start_date)
        if end_date:
            conditions.append(StockTradingDaily.trade_date <= end_date)

        stmt = select(StockTradingDaily).where(
            and_(*conditions)
        ).order_by(
            StockTradingDaily.trade_date.desc()
        ).offset(skip).limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def count_stock_history(
        self,
        stock_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> int:
        """특정 종목의 거래 히스토리 개수 조회

        Args:
            stock_code: 종목코드
            start_date: 시작일자
            end_date: 종료일자

        Returns:
            전체 개수
        """
        conditions = [StockTradingDaily.stock_code == stock_code]

        if start_date:
            conditions.append(StockTradingDaily.trade_date >= start_date)
        if end_date:
            conditions.append(StockTradingDaily.trade_date <= end_date)

        stmt = select(func.count(StockTradingDaily.id)).where(
            and_(*conditions)
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def delete_by_date(self, trade_date: date) -> int:
        """특정 날짜의 거래 정보 삭제

        Args:
            trade_date: 거래일자

        Returns:
            삭제된 개수
        """
        stmt = delete(StockTradingDaily).where(
            StockTradingDaily.trade_date == trade_date
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
