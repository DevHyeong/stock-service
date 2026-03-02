from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.domain.chart.dto.response.chart_item import (
    MinuteChartResponse,
    DayChartResponse,
    DayChartWithMAResponse,
    WeekChartResponse,
    MonthChartResponse,
    BatchSyncResponse,
)
from app.domain.chart.services.chart_service import ChartService
from app.containers import Container

router = APIRouter(prefix="/chart", tags=["차트 데이터 (키움)"])


# ── 배치 동기화 (전체 종목) ───────────────────────────────────────────────────

@router.post("/batch/minute", response_model=BatchSyncResponse)
@inject
async def batch_sync_minute_chart(
    base_dt: Optional[str] = Query(None, description="기준일자 (YYYYMMDD), 미입력 시 당일"),
    tic_scope: str = Query("1", description="틱범위: 1, 3, 5, 10, 15, 30, 45, 60"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''전체 종목 분봉 차트 배치 동기화

    DB에 등록된 모든 활성 종목의 분봉 데이터를 Kiwoom API에서 가져와 저장합니다.
    자동 페이징을 지원하여 전체 이력 데이터를 한 번에 적재합니다.
    '''
    return await chart_service.batch_sync_minute_chart(
        base_dt=base_dt,
        tic_scope=tic_scope,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


@router.post("/batch/day", response_model=BatchSyncResponse)
@inject
async def batch_sync_day_chart(
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''전체 종목 일봉 차트 배치 동기화

    DB에 등록된 모든 활성 종목의 일봉 데이터를 Kiwoom API에서 가져와 저장합니다.
    자동 페이징을 지원하여 전체 이력 데이터를 한 번에 적재합니다.
    '''
    return await chart_service.batch_sync_day_chart(
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


@router.post("/batch/week", response_model=BatchSyncResponse)
@inject
async def batch_sync_week_chart(
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''전체 종목 주봉 차트 배치 동기화

    DB에 등록된 모든 활성 종목의 주봉 데이터를 Kiwoom API에서 가져와 저장합니다.
    자동 페이징을 지원하여 전체 이력 데이터를 한 번에 적재합니다.
    '''
    return await chart_service.batch_sync_week_chart(
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


@router.post("/batch/month", response_model=BatchSyncResponse)
@inject
async def batch_sync_month_chart(
    base_dt: str = Query(..., description="기준일자 (YYYYMMDD)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''전체 종목 월봉 차트 배치 동기화

    DB에 등록된 모든 활성 종목의 월봉 데이터를 Kiwoom API에서 가져와 저장합니다.
    자동 페이징을 지원하여 전체 이력 데이터를 한 번에 적재합니다.
    '''
    return await chart_service.batch_sync_month_chart(
        base_dt=base_dt,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


# ── 날짜 범위 동기화 (단건 or 전체 종목) ──────────────────────────────────────

@router.post("/sync/minute", response_model=BatchSyncResponse)
@inject
async def sync_minute_chart_range(
    start_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    stock_code: Optional[str] = Query(None, description="종목코드 (미입력 시 전체 종목)"),
    tic_scope: str = Query("1", description="틱범위: 1, 3, 5, 10, 15, 30, 45, 60"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''분봉 날짜 범위 동기화

    지정한 기간(start_dt ~ end_dt)의 분봉 데이터를 Kiwoom API에서 가져와 DB에 저장합니다.
    stock_code 미입력 시 DB에 등록된 모든 활성 종목을 처리합니다.
    '''
    return await chart_service.sync_minute_chart_range(
        start_dt=start_dt,
        end_dt=end_dt,
        stock_code=stock_code,
        tic_scope=tic_scope,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


@router.post("/sync/day", response_model=BatchSyncResponse)
@inject
async def sync_day_chart_range(
    start_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    stock_code: Optional[str] = Query(None, description="종목코드 (미입력 시 전체 종목)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''일봉 날짜 범위 동기화

    지정한 기간(start_dt ~ end_dt)의 일봉 데이터를 Kiwoom API에서 가져와 DB에 저장합니다.
    stock_code 미입력 시 DB에 등록된 모든 활성 종목을 처리합니다.
    '''
    return await chart_service.sync_day_chart_range(
        start_dt=start_dt,
        end_dt=end_dt,
        stock_code=stock_code,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


@router.post("/sync/week", response_model=BatchSyncResponse)
@inject
async def sync_week_chart_range(
    start_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    stock_code: Optional[str] = Query(None, description="종목코드 (미입력 시 전체 종목)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''주봉 날짜 범위 동기화

    지정한 기간(start_dt ~ end_dt)의 주봉 데이터를 Kiwoom API에서 가져와 DB에 저장합니다.
    stock_code 미입력 시 DB에 등록된 모든 활성 종목을 처리합니다.
    '''
    return await chart_service.sync_week_chart_range(
        start_dt=start_dt,
        end_dt=end_dt,
        stock_code=stock_code,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


@router.post("/sync/month", response_model=BatchSyncResponse)
@inject
async def sync_month_chart_range(
    start_dt: str = Query(..., description="시작일자 (YYYYMMDD)"),
    end_dt: str = Query(..., description="종료일자 (YYYYMMDD)"),
    stock_code: Optional[str] = Query(None, description="종목코드 (미입력 시 전체 종목)"),
    upd_stkpc_tp: str = Query("1", description="수정주가구분: 0(미적용), 1(적용)"),
    delay: float = Query(0.5, description="종목 간 API 호출 딜레이(초)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> BatchSyncResponse:
    '''월봉 날짜 범위 동기화

    지정한 기간(start_dt ~ end_dt)의 월봉 데이터를 Kiwoom API에서 가져와 DB에 저장합니다.
    stock_code 미입력 시 DB에 등록된 모든 활성 종목을 처리합니다.
    '''
    return await chart_service.sync_month_chart_range(
        start_dt=start_dt,
        end_dt=end_dt,
        stock_code=stock_code,
        upd_stkpc_tp=upd_stkpc_tp,
        delay=delay,
    )


# ── 단건 조회/동기화 (경로 파라미터는 반드시 정적 경로보다 뒤에 위치) ──────────

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


@router.get("/{stock_code}/day/ma", response_model=DayChartWithMAResponse)
@inject
async def get_day_chart_with_ma(
    stock_code: str,
    start_dt: str = Query(..., description="조회 시작일 (YYYYMMDD)"),
    end_dt: str = Query(..., description="조회 종료일 (YYYYMMDD)"),
    chart_service: ChartService = Depends(Provide[Container.chart_service]),
) -> DayChartWithMAResponse:
    '''일봉 차트 + 5/10/20/60 이동평균선 조회

    DB에 저장된 일봉 데이터를 기반으로 5, 10, 20, 60일 이동평균선을 계산하여 반환합니다.
    선행 데이터가 부족한 초기 구간은 해당 MA 값이 null로 반환됩니다.
    '''
    return await chart_service.get_day_chart_with_ma(
        stk_cd=stock_code,
        start_dt=start_dt,
        end_dt=end_dt,
    )


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
