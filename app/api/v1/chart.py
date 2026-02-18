from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.domain.chart.dto.response.chart_item import (
    MinuteChartResponse,
    DayChartResponse,
    WeekChartResponse,
    MonthChartResponse,
)
from app.domain.chart.services.chart_service import ChartService
from app.containers import Container

router = APIRouter(prefix="/chart", tags=["차트 데이터 (키움)"])


# ── 분봉 ──────────────────────────────────────────────────────────────────────

@router.post("/{stock_code}/minute", response_model=MinuteChartResponse)
@inject
async def sync_minute_chart(
    stock_code: str,
    tic_scope: str = Query("1", description="틱범위: 1, 3, 5, 10, 15, 30, 45, 60"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    base_dt: Optional[str] = Query(None, description="기준일자 (YYYYMMDD)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> MinuteChartResponse:
    '''분봉 차트 조회 및 저장 (ka10080)

    Kiwoom API에서 분봉 데이터를 가져와 DB에 저장합니다.
    '''
    return await chart_service.sync_minute_chart(
        stk_cd=stock_code,
        tic_scope=tic_scope,
        upd_stkpc_tp=upd_stkpc_tp,
        base_dt=base_dt,
        cont_yn=cont_yn,
        next_key=next_key,
    )


@router.get("/{stock_code}/minute", response_model=MinuteChartResponse)
@inject
async def get_minute_chart(
    stock_code: str,
    date: str = Query(..., description="조회 날짜 (YYYYMMDD)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> MinuteChartResponse:
    '''분봉 차트 DB 조회

    DB에 저장된 분봉 데이터를 반환합니다.
    '''
    return await chart_service.get_minute_chart(stk_cd=stock_code, date=date)


# ── 일봉 ──────────────────────────────────────────────────────────────────────

@router.post("/{stock_code}/day", response_model=DayChartResponse)
@inject
async def sync_day_chart(
    stock_code: str,
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> DayChartResponse:
    '''일봉 차트 조회 및 저장 (ka10081)

    Kiwoom API에서 일봉 데이터를 가져와 DB에 저장합니다.
    '''
    return await chart_service.sync_day_chart(
        stk_cd=stock_code,
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        cont_yn=cont_yn,
        next_key=next_key,
    )


@router.get("/{stock_code}/day", response_model=DayChartResponse)
@inject
async def get_day_chart(
    stock_code: str,
    start_dt: str = Query(..., description="조회 시작일 (YYYYMMDD)"),
    end_dt: str = Query(..., description="조회 종료일 (YYYYMMDD)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> DayChartResponse:
    '''일봉 차트 DB 조회

    DB에 저장된 일봉 데이터를 반환합니다.
    '''
    return await chart_service.get_day_chart(stk_cd=stock_code, start_dt=start_dt, end_dt=end_dt)


# ── 주봉 ──────────────────────────────────────────────────────────────────────

@router.post("/{stock_code}/week", response_model=WeekChartResponse)
@inject
async def sync_week_chart(
    stock_code: str,
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> WeekChartResponse:
    '''주봉 차트 조회 및 저장 (ka10082)

    Kiwoom API에서 주봉 데이터를 가져와 DB에 저장합니다.
    '''
    return await chart_service.sync_week_chart(
        stk_cd=stock_code,
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        cont_yn=cont_yn,
        next_key=next_key,
    )


@router.get("/{stock_code}/week", response_model=WeekChartResponse)
@inject
async def get_week_chart(
    stock_code: str,
    start_dt: str = Query(..., description="조회 시작일 (YYYYMMDD)"),
    end_dt: str = Query(..., description="조회 종료일 (YYYYMMDD)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> WeekChartResponse:
    '''주봉 차트 DB 조회

    DB에 저장된 주봉 데이터를 반환합니다.
    '''
    return await chart_service.get_week_chart(stk_cd=stock_code, start_dt=start_dt, end_dt=end_dt)


# ── 월봉 ──────────────────────────────────────────────────────────────────────

@router.post("/{stock_code}/month", response_model=MonthChartResponse)
@inject
async def sync_month_chart(
    stock_code: str,
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> MonthChartResponse:
    '''월봉 차트 조회 및 저장 (ka10083)

    Kiwoom API에서 월봉 데이터를 가져와 DB에 저장합니다.
    '''
    return await chart_service.sync_month_chart(
        stk_cd=stock_code,
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        cont_yn=cont_yn,
        next_key=next_key,
    )


@router.get("/{stock_code}/month", response_model=MonthChartResponse)
@inject
async def get_month_chart(
    stock_code: str,
    start_dt: str = Query(..., description="조회 시작일 (YYYYMMDD)"),
    end_dt: str = Query(..., description="조회 종료일 (YYYYMMDD)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> MonthChartResponse:
    '''월봉 차트 DB 조회

    DB에 저장된 월봉 데이터를 반환합니다.
    '''
    return await chart_service.get_month_chart(stk_cd=stock_code, start_dt=start_dt, end_dt=end_dt)
