from app.db import AsyncSessionLocal
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.stock.repositories.investor_daily_trade_repository import InvestorDailyTradeRepository


class StockUnitOfWork(AbstractUnitOfWork):
    async def _begin(self):
        self.session = AsyncSessionLocal()
        self.investor_daily_trade_repo = InvestorDailyTradeRepository(self.session)

    async def _close(self):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
