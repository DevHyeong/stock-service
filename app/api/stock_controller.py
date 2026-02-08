# app/api/rank_controller.py
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.containers import Container
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/investor-daily-trade", response_model=InvestorDailyTradeStock)
@inject
async def get_investor_daily_trade_stock(
    strt_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    trde_tp: str = Query(..., description="매매구분 (1: 순매도, 2: 순매수)"),
    mrkt_tp: str = Query(..., description="시장구분 (001: 코스피, 101: 코스닥)"),
    invsr_tp: str = Query(..., description="투자자구분 (8000: 개인, 9000: 외국인, ...)"),
    stex_tp: str = Query(..., description="거래소구분 (1: KRX, 2: NXT, 3: 통합)"),
    stock_service: StockService = Depends(Provide[Container.stock_service])
) -> List[InvestorDailyTradeStock]:
    return await stock_service.get_investor_daily_trade_stock(
        investorDailyTradeStockRequest=InvestorDailyTradeStockRequest(
            strt_dt=strt_dt,
            end_dt=end_dt,
            trde_tp=trde_tp,
            mrkt_tp=mrkt_tp,
            invsr_tp=invsr_tp,
            stex_tp=stex_tp
        )
    )
