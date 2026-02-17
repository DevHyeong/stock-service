from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.repositories.investor_daily_trade_repository import InvestorDailyTradeRepository
from app.domain.stock.repositories.stock_api_repository import StockApiRepository


class StockService:
    def __init__(self, stock_repository: StockApiRepository):
        self.stock_repository = stock_repository

    async def get_investor_daily_trade_stock(
        self,
        investorDailyTradeStockRequest: InvestorDailyTradeStockRequest,
        db: Optional[AsyncSession] = None
    ) -> List[InvestorDailyTradeStock]:
        trades = await self.stock_repository.get_investor_daily_trade_stock(investorDailyTradeStockRequest)

        if db is not None:
            repo = InvestorDailyTradeRepository(db)
            await repo.bulk_upsert(trades, investorDailyTradeStockRequest)

        return trades
