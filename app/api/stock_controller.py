# app/api/stock_controller.py
from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.containers import Container
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.domain.stock.dto.stock_basic_info import StockBasicInfoRequest
from app.domain.stock.services.stock_service import StockService
from app.schemas.response import APIResponse

router = APIRouter(prefix="/stock", tags=["stock"])


@router.post("/basic-info/sync")
@inject
async def sync_stock_basic_info(
    stk_cd: str = Query(..., description="종목코드 (예: 005930)"),
    stock_sync_service: StockService = Depends(Provide[Container.stock_service]),
):
    try:
        result = await stock_sync_service.sync_stock_basic_info(
            request=StockBasicInfoRequest(stk_cd=stk_cd)
        )
        return APIResponse(
            success=True,
            message=f"주식 기본 정보 동기화 완료: {result.stk_nm}({result.stk_cd})",
            data=result.model_dump(by_alias=True),
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="주식 기본 정보 동기화 실패",
            error=str(e)
        )


@router.post("/investor-daily-trade/sync")
@inject
async def sync_investor_daily_trade_stock(
    strt_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    trde_tp: Optional[str] = Query(None, description="매매구분 (1: 순매도, 2: 순매수)"),
    mrkt_tp: Optional[str] = Query(None, description="시장구분 (001: 코스피, 101: 코스닥)"),
    invsr_tp: Optional[str] = Query(None, description="투자자구분 (8000: 개인, 9000: 외국인, ...)"),
    stex_tp: Optional[str] = Query(None, description="거래소구분 (1: KRX, 2: NXT, 3: 통합)"),
    stock_sync_service: StockService = Depends(Provide[Container.stock_service]),
):
    try:
        result = await stock_sync_service.sync_investor_daily_trade_stock(
            investorDailyTradeStockRequest=InvestorDailyTradeStockRequest(
                strt_dt=strt_dt,
                end_dt=end_dt,
                trde_tp=trde_tp,
                mrkt_tp=mrkt_tp,
                invsr_tp=invsr_tp,
                stex_tp=stex_tp
            )
        )
        return APIResponse(
            success=True,
            message=f"투자자별 일별 매매 동기화 완료: {len(result)}건",
            data=[r.model_dump() for r in result]
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="투자자별 일별 매매 동기화 실패",
            error=str(e)
        )


@router.get("/investor-daily-trade")
@inject
async def get_investor_daily_trade_stock(
    strt_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    trde_tp: str = Query(..., description="매매구분 (1: 순매도, 2: 순매수)"),
    mrkt_tp: str = Query(..., description="시장구분 (001: 코스피, 101: 코스닥)"),
    invsr_tp: str = Query(..., description="투자자구분 (8000: 개인, 9000: 외국인, ...)"),
    stex_tp: str = Query(..., description="거래소구분 (1: KRX, 2: NXT, 3: 통합)"),
    stock_sync_service: StockService = Depends(Provide[Container.stock_service]),
):
    try:
        result = await stock_sync_service.get_investor_daily_trade_stock(
            request=InvestorDailyTradeStockRequest(
                strt_dt=strt_dt,
                end_dt=end_dt,
                trde_tp=trde_tp,
                mrkt_tp=mrkt_tp,
                invsr_tp=invsr_tp,
                stex_tp=stex_tp
            )
        )
        return APIResponse(
            success=True,
            message="투자자별 일별 매매 조회 성공",
            data=[r.model_dump() for r in result]
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="투자자별 일별 매매 조회 실패",
            error=str(e)
        )
