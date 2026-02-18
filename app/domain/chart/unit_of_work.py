from app.db import AsyncSessionLocal
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.chart.repositories.chart_db_repository import ChartDbRepository


class ChartUnitOfWork(AbstractUnitOfWork):
    async def _begin(self):
        self.session = AsyncSessionLocal()
        self.chart_repo = ChartDbRepository(self.session)

    async def _close(self):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
