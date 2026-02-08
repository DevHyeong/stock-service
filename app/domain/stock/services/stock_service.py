from typing import List

from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.repositories.stock_api_repository import StockApiRepository


class StockService:
    def __init__(self, stock_repository: StockApiRepository):
        self.stock_repository = stock_repository

    async def get_investor_daily_trade_stock(
        self,
        investorDailyTradeStockRequest: InvestorDailyTradeStockRequest
    ) -> List[InvestorDailyTradeStock]:
        return await self.stock_repository.get_investor_daily_trade_stock(investorDailyTradeStockRequest)