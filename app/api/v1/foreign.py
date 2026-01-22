from fastapi import APIRouter, Depends, Query
from app.schemas.response import APIResponse
from app.services.kiwoom_service import KiwoomService
from app.api.deps import get_kiwoom_service
from typing import Optional

router = APIRouter(prefix="/foreign", tags=["외국인 매매동향"])


@router.get("/trading")
async def get_foreign_trading(
        stock_code: str = Query(..., min_length=6, max_length=6, description="종목코드"),
        date: Optional[str] = Query(None, regex=r'^\d{8}$', description="조회일자 (YYYYMMDD)"),
        direction: str = Query("0", description="정렬구분 (0:순매수상위, 1:순매도상위)"),
        kiwoom_service: KiwoomService = Depends(get_kiwoom_service)
):
    '''주식외국인종목별매매동향 조회'''
    try:
        result = await kiwoom_service.get_foreign_trading(
            stock_code=stock_code,
            date=date,
            direction=direction
        )
        return APIResponse(
            success=True,
            message="조회 성공",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="조회 실패",
            error=str(e)
        )


@router.post("/trading/multiple")
async def get_multiple_foreign_trading(
        stock_codes: list[str],
        kiwoom_service: KiwoomService = Depends(get_kiwoom_service)
):
    '''여러 종목 외국인 매매동향 동시 조회'''
    try:
        result = await kiwoom_service.get_multiple_stocks_trading(stock_codes)
        return APIResponse(
            success=True,
            message="조회 성공",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="조회 실패",
            error=str(e)
        )