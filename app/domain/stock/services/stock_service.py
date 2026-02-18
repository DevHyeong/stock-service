from typing import List

from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.repositories.stock_api_repository import StockApiRepository
from app.domain.stock.unit_of_work import StockUnitOfWork


class StockService:
    def __init__(self, stock_repository: StockApiRepository):
        self.stock_repository = stock_repository

    async def sync_investor_daily_trade_stock(
        self,
        investorDailyTradeStockRequest: InvestorDailyTradeStockRequest,
    ) -> List[InvestorDailyTradeStock]:
        trades = await self.stock_repository.get_investor_daily_trade_stock(investorDailyTradeStockRequest)

        async with StockUnitOfWork() as uow:
            await uow.investor_daily_trade_repo.bulk_upsert(trades, investorDailyTradeStockRequest)
            await uow.commit()

        return trades

    async def get_investor_daily_trade_stock(
        self,
        request: InvestorDailyTradeStockRequest,
    ) -> List[InvestorDailyTradeStock]:
        async with StockUnitOfWork() as uow:
            return await uow.investor_daily_trade_repo.get_by_request(request)
