# 사용 예시 (repository/stock_repository.py)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import Stock


class StockRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_code(self, code: str):
        # JPA의 findByCode()와 유사
        result = await self.db.execute(
            select(Stock).where(Stock.code == code)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100, market_code: str = None):
        """DB에서 종목 리스트 조회

        Args:
            skip: 건너뛸 개수 (페이지네이션)
            limit: 조회할 개수
            market_code: 시장구분 (0: KOSPI, 1: KOSDAQ)

        Returns:
            종목 리스트
        """
        query = select(Stock)

        if market_code is not None:
            query = query.where(Stock.market_code == market_code)

        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_all(self, market_code: str = None):
        """전체 종목 수 카운트

        Args:
            market_code: 시장구분 필터

        Returns:
            종목 수
        """
        from sqlalchemy import func

        query = select(func.count(Stock.code))

        if market_code is not None:
            query = query.where(Stock.market_code == market_code)

        result = await self.db.execute(query)
        return result.scalar()

    # async def save(self, stock: Stock):
    #     # JPA의 save()와 유사
    #     self.db.add(stock)
    #     await self.db.commit()
    #     await self.db.refresh(stock)
    #     return stock

    async def save_all(self, stocks: list[Stock]):
        self.db.add_all(stocks)
        await self.db.commit()

        # refresh는 선택사항 (ID가 필요한 경우)
        for stock in stocks:
            await self.db.refresh(stock)

        return stocks
