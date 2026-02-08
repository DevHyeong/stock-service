from typing import List

from app.common.auth_client import AuthClient
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.repositories.stock_client import StockClient


class StockApiRepository:
    def __init__(self, auth_client: AuthClient, stock_client: StockClient):
        self.auth_client = auth_client
        self.stock_client = stock_client

    async def get_investor_daily_trade_stock(
        self,
        investorDailyTradeStockRequest: InvestorDailyTradeStockRequest
    ) -> List[InvestorDailyTradeStock]:
        return await self.stock_client.get_investor_daily_trade_stock(
            access_token = await self.auth_client.ensure_token(),
            investorDailyTradeStockRequest = investorDailyTradeStockRequest
        )