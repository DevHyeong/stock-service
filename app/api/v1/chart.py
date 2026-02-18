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


@router.get("/{stock_code}/minute", response_model=MinuteChartResponse)
@inject
async def get_minute_chart(
    stock_code: str,
    tic_scope: str = Query("1", description="틱범위: 1, 3, 5, 10, 15, 30, 45, 60"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    base_dt: Optional[str] = Query(None, description="기준일자 (YYYYMMDD)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> MinuteChartResponse:
    '''분봉차트 조회 (ka10080)

    주식의 분 단위 차트 데이터를 조회합니다.

    Args:
        stock_code: 종목코드 (예: 005930)
        tic_scope: 틱범위 (1, 3, 5, 10, 15, 30, 45, 60분)
        upd_stkpc_tp: 수정주가구분 (0: 미적용, 1: 적용)
        base_dt: 기준일자 (YYYYMMDD, 생략 시 최근 데이터)
        cont_yn: 연속조회여부
        next_key: 연속조회키

    Returns:
        분봉 OHLCV 데이터 리스트
    '''
    return await chart_service.get_minute_chart(
        stk_cd=stock_code,
        tic_scope=tic_scope,
        upd_stkpc_tp=upd_stkpc_tp,
        base_dt=base_dt,
        cont_yn=cont_yn,
        next_key=next_key,
    )


@router.get("/{stock_code}/day", response_model=DayChartResponse)
@inject
async def get_day_chart(
    stock_code: str,
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> DayChartResponse:
    '''일봉차트 조회 (ka10081)

    주식의 일 단위 차트 데이터를 조회합니다.

    Args:
        stock_code: 종목코드 (예: 005930)
        base_dt: 기준일자 (YYYYMMDD)
        upd_stkpc_tp: 수정주가구분 (0: 미적용, 1: 적용)
        cont_yn: 연속조회여부
        next_key: 연속조회키

    Returns:
        일봉 OHLCV 데이터 리스트
    '''
    return await chart_service.get_day_chart(
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
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> WeekChartResponse:
    '''주봉차트 조회 (ka10082)

    주식의 주 단위 차트 데이터를 조회합니다.

    Args:
        stock_code: 종목코드 (예: 005930)
        base_dt: 기준일자 (YYYYMMDD)
        upd_stkpc_tp: 수정주가구분 (0: 미적용, 1: 적용)
        cont_yn: 연속조회여부
        next_key: 연속조회키

    Returns:
        주봉 OHLCV 데이터 리스트
    '''
    return await chart_service.get_week_chart(
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
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    cont_yn: Optional[str] = Query(None, description="연속조회여부"),
    next_key: Optional[str] = Query(None, description="연속조회키"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> MonthChartResponse:
    '''월봉차트 조회 (ka10083)

    주식의 월 단위 차트 데이터를 조회합니다.

    Args:
        stock_code: 종목코드 (예: 005930)
        base_dt: 기준일자 (YYYYMMDD)
        upd_stkpc_tp: 수정주가구분 (0: 미적용, 1: 적용)
        cont_yn: 연속조회여부
        next_key: 연속조회키

    Returns:
        월봉 OHLCV 데이터 리스트
    '''
    return await chart_service.get_month_chart(
        stk_cd=stock_code,
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        cont_yn=cont_yn,
        next_key=next_key,
    )
