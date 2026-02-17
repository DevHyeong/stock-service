
from fastapi import APIRouter, Depends, Query
from app.schemas.response import APIResponse
from app.services.kiwoom_service import KiwoomService
from app.api.deps import get_kiwoom_service

router = APIRouter(prefix="/market", tags=["실시간 시세정보 (키움)"])


@router.get("/execution/{stock_code}")
async def get_execution_info(
        stock_code: str,
        kiwoom_service: KiwoomService = Depends(get_kiwoom_service)
):
    '''체결정보 조회 (ka10003)

    실시간 체결 정보를 조회합니다.

    Args:
        stock_code: 종목코드 (예: 005930)

    Returns:
        체결정보 리스트 (시간, 현재가, 거래량, 체결강도 등)
    '''
    try:
        result = await kiwoom_service.get_execution_info(stock_code=stock_code)
        return APIResponse(
            success=True,
            message="체결정보 조회 성공",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="체결정보 조회 실패",
            error=str(e)
        )


@router.get("/bidask/{stock_code}")
async def get_bid_ask(
        stock_code: str,
        kiwoom_service: KiwoomService = Depends(get_kiwoom_service)
):
    '''호가정보 조회 (ka10004)

    실시간 매수/매도 호가 정보를 조회합니다.

    Args:
        stock_code: 종목코드 (예: 005930)

    Returns:
        10단계 매수/매도 호가 정보
    '''
    try:
        result = await kiwoom_service.get_bid_ask(stock_code=stock_code)
        return APIResponse(
            success=True,
            message="호가정보 조회 성공",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="호가정보 조회 실패",
            error=str(e)
        )
