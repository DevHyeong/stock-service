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
