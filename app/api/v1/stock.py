from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories.stock_repository import StockRepository
from app.schemas.response import APIResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["종목 관리"])

def get_stock_service(db: AsyncSession = Depends(get_db)) -> StockService:
    repo = StockRepository(db)
    return StockService(repo)


@router.get("/list")
async def get_stock_list(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="조회 개수"),
    market_code: str = Query(None, description="시장구분 (0: KOSPI, 1: KOSDAQ)"),
    stock_service: StockService = Depends(get_stock_service)
):
    """종목 리스트 조회

    DB에 저장된 종목 리스트를 조회합니다.

    Args:
        skip: 페이지네이션 오프셋
        limit: 페이지네이션 리미트
        market_code: 시장구분 필터 (0: KOSPI, 1: KOSDAQ)

    Returns:
        종목 리스트와 전체 개수
    """
    try:
        result = await stock_service.get_stock_list(
            skip=skip,
            limit=limit,
            market_code=market_code
        )
        return APIResponse(
            success=True,
            message="종목 리스트 조회 성공",
            data=result.model_dump()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="종목 리스트 조회 실패",
            error=str(e)
        )


@router.post("/sync")
async def sync_stock_list(
    market_code: str = Query("0", description="시장구분 (0: KOSPI, 1: KOSDAQ, 빈 문자열: 전체)"),
    stock_service: StockService = Depends(get_stock_service)
):
    """종목 리스트 동기화

    키움 API에서 종목 리스트를 가져와 DB에 저장합니다.

    Args:
        market_code: 시장구분 (0: KOSPI, 1: KOSDAQ, 빈 문자열: 전체)

    Returns:
        동기화 결과 (저장된 종목 수)
    """
    try:
        result = await stock_service.sync_stock_list(market_code=market_code)
        return APIResponse(
            success=True,
            message=f"종목 리스트 동기화 완료: {result['synced_count']}건",
            data=result
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="종목 리스트 동기화 실패",
            error=str(e)
        )