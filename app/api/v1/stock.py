from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories.stock_repository import StockRepository
from app.schemas.response import APIResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["외국인 매매동향"])

def get_stock_service(db: AsyncSession = Depends(get_db)) -> StockService:
    repo = StockRepository(db)
    return StockService(repo)

@router.get("/list")
async def get_foreign_trading(
    stock_service: StockService = Depends(get_stock_service)
):
    result = await stock_service.get_stock_list()
    return APIResponse(
        success=True,
        message="조회 성공",
        data=result
    )