from itertools import product
from typing import List

from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.dto.stock_basic_info import StockBasicInfo, StockBasicInfoRequest
from app.domain.stock.repositories.stock_api_repository import StockApiRepository
from app.domain.stock.unit_of_work import StockUnitOfWork

TRADE_TYPES = ["1", "2"]  # 순매도, 순매수
MARKET_TYPES = ["001", "101"]  # 코스피, 코스닥
INVESTOR_TYPES = ["8000", "9000", "1000", "3000", "3100", "5000", "4000", "2000", "6000", "7000", "7100", "9999"]
EXCHANGE_TYPES = ["1", "2", "3"]  # KRX, NXT, 통합


class StockService:
    def __init__(self, stock_repository: StockApiRepository):
        self.stock_repository = stock_repository

    async def sync_investor_daily_trade_stock(
        self,
        investorDailyTradeStockRequest: InvestorDailyTradeStockRequest,
    ) -> List[InvestorDailyTradeStock]:
        trde_tps = [investorDailyTradeStockRequest.trde_tp] if investorDailyTradeStockRequest.trde_tp else TRADE_TYPES
        mrkt_tps = [investorDailyTradeStockRequest.mrkt_tp] if investorDailyTradeStockRequest.mrkt_tp else MARKET_TYPES
        invsr_tps = [investorDailyTradeStockRequest.invsr_tp] if investorDailyTradeStockRequest.invsr_tp else INVESTOR_TYPES
        stex_tps = [investorDailyTradeStockRequest.stex_tp] if investorDailyTradeStockRequest.stex_tp else EXCHANGE_TYPES

        all_trades: List[InvestorDailyTradeStock] = []

        async with StockUnitOfWork() as uow:
            for trde_tp, mrkt_tp, invsr_tp, stex_tp in product(trde_tps, mrkt_tps, invsr_tps, stex_tps):
                req = InvestorDailyTradeStockRequest(
                    strt_dt=investorDailyTradeStockRequest.strt_dt,
                    end_dt=investorDailyTradeStockRequest.end_dt,
                    trde_tp=trde_tp,
                    mrkt_tp=mrkt_tp,
                    invsr_tp=invsr_tp,
                    stex_tp=stex_tp,
                )
                trades = await self.stock_repository.get_investor_daily_trade_stock(req)
                if trades:
                    await uow.investor_daily_trade_repo.bulk_upsert(trades, req)
                    all_trades.extend(trades)

            await uow.commit()

        return all_trades

    async def sync_stock_basic_info(
        self,
        request: StockBasicInfoRequest,
    ) -> StockBasicInfo:
        info = await self.stock_repository.get_stock_basic_info(request)

        async with StockUnitOfWork() as uow:
            await uow.stock_basic_info_repo.upsert(info)
            await uow.commit()

        return info

    async def get_investor_daily_trade_stock(
        self,
        request: InvestorDailyTradeStockRequest,
    ) -> List[InvestorDailyTradeStock]:
        async with StockUnitOfWork() as uow:
            return await uow.investor_daily_trade_repo.get_by_request(request)
