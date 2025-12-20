from fastapi import APIRouter, Depends

from app.models.response import APIResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["외국인 매매동향"])

@router.get("/list")
async def get_foreign_trading(
    stock_service: StockService = Depends(StockService)
):
    result = await stock_service.get_stock_list()
    return APIResponse(
        success=True,
        message="조회 성공",
        data=result
    )