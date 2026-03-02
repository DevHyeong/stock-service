from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.db import get_db
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStockRequest
from app.domain.stock.dto.stock_basic_info import StockBasicInfoRequest
from app.repositories.stock_repository import StockRepository
from app.schemas.response import APIResponse
from app.schemas.enums import MarketCode
from app.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["종목 관리"])

def get_stock_service(db: AsyncSession = Depends(get_db)) -> StockService:
    repo = StockRepository(db)
    return StockService(repo)


@router.get("/list")
async def get_stock_list(
    skip: int = Query(0, ge=0, description="건너뛸 개수 (페이지네이션)"),
    limit: int = Query(100, ge=1, le=1000, description="조회 개수 (최대 1000)"),
    market_code: Optional[MarketCode] = Query(None, description="시장구분 (0: KOSPI, 10: KOSDAQ, 등)"),
    start_date: Optional[str] = Query(None, description="조회 시작일 (YYYY-MM-DD, created_at 기준)", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, description="조회 종료일 (YYYY-MM-DD, created_at 기준)", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    order_by: Optional[str] = Query(
        None,
        description="정렬 기준",
        pattern="^(market_cap_desc|market_cap_asc|created_at_desc|created_at_asc|name_asc|name_desc)$"
    ),
    stock_service: StockService = Depends(get_stock_service)
):
    """종목 리스트 조회 (페이지네이션, 필터, 정렬 지원)

    DB에 저장된 종목 리스트를 조회합니다.

    **페이지네이션:**
    - skip: 건너뛸 개수 (0부터 시작)
    - limit: 조회할 개수 (최대 1000)

    **필터:**
    - market_code: 시장구분 (0: KOSPI, 10: KOSDAQ, 30: K-OTC, 50: KONEX, 8: ETF, 60: ETN)
    - start_date: 종목 등록 시작일 (created_at 기준)
    - end_date: 종목 등록 종료일 (created_at 기준)

    **정렬:**
    - market_cap_desc: 시가총액 내림차순 (큰 값부터)
    - market_cap_asc: 시가총액 오름차순 (작은 값부터)
    - created_at_desc: 등록일 내림차순 (최신순)
    - created_at_asc: 등록일 오름차순 (과거순)
    - name_asc: 종목명 오름차순 (ㄱ-ㅎ)
    - name_desc: 종목명 내림차순 (ㅎ-ㄱ)

    **사용 예시:**
    - 시가총액 상위 100개: `?limit=100&order_by=market_cap_desc`
    - 코스피 최신 등록 종목: `?market_code=0&order_by=created_at_desc`
    - 2026년 1월 등록된 종목: `?start_date=2026-01-01&end_date=2026-01-31`

    Args:
        skip: 페이지네이션 오프셋
        limit: 페이지네이션 리미트
        market_code: 시장구분 필터
        start_date: 조회 시작일 (YYYY-MM-DD)
        end_date: 조회 종료일 (YYYY-MM-DD)
        order_by: 정렬 기준

    Returns:
        종목 리스트와 전체 개수
    """
    try:
        result = await stock_service.get_stock_list(
            skip=skip,
            limit=limit,
            market_code=market_code.value if market_code else None,
            start_date=start_date,
            end_date=end_date,
            order_by=order_by,
        )
        return APIResponse(
            success=True,
            message="종목 리스트 조회 성공",
            data=result.model_dump()
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(
            success=False,
            message="종목 리스트 조회 실패",
            error=str(e)
        )


@router.get("/basic-info")
@inject
async def get_stock_basic_info(
    stk_cd: str = Query(..., description="종목코드 (예: 005930)"),
    stock_service: StockService = Depends(Provide[Container.stock_service]),
):
    """주식 기본정보 조회

    DB에 동기화된 주식 기본정보를 조회합니다.

    Args:
        stk_cd: 종목코드 (예: 005930)

    Returns:
        주식 기본정보 (종목명, 현재가, 시가, 고가, 저가, PER, PBR, EPS 등)
    """
    try:
        result = await stock_service.get_stock_basic_info(stk_cd=stk_cd)
        if result is None:
            return APIResponse(
                success=False,
                message=f"종목을 찾을 수 없습니다: {stk_cd}",
                error="NOT_FOUND"
            )
        return APIResponse(
            success=True,
            message=f"주식 기본정보 조회 성공: {result.stk_nm}({result.stk_cd})",
            data=result.model_dump(by_alias=True),
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="주식 기본정보 조회 실패",
            error=str(e)
        )


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

