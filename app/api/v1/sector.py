from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.response import APIResponse
from app.schemas.sector import SectorCreate, SectorUpdate
from app.services.sector_service import sector_service
from app.domain.sector.repositories.sector_repository import SectorRepository
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/sector", tags=["섹터/업종 관리"])


@router.get("/list")
async def get_sectors(
        market: Optional[str] = Query(None, description="시장구분 (KOSPI, KOSDAQ)"),
        category: Optional[str] = Query(None, description="카테고리"),
        skip: int = Query(0, ge=0, description="건너뛸 개수"),
        limit: int = Query(100, ge=1, le=1000, description="조회 개수"),
        db: AsyncSession = Depends(get_db)
):
    '''섹터 리스트 조회

    DB에 저장된 섹터/업종 리스트를 조회합니다.

    Args:
        market: 시장구분 필터
        category: 카테고리 필터
        skip: 페이지네이션 오프셋
        limit: 페이지네이션 리미트

    Returns:
        섹터 리스트
    '''
    try:
        result = await sector_service.get_all_sectors(
            db,
            market=market,
            category=category,
            skip=skip,
            limit=limit
        )

        return APIResponse(
            success=True,
            message="섹터 리스트 조회 성공",
            data=result.model_dump()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="섹터 리스트 조회 실패",
            error=str(e)
        )


@router.get("/{sector_code}")
async def get_sector_detail(
        sector_code: str,
        db: AsyncSession = Depends(get_db)
):
    '''섹터 상세 정보 조회 (종목 포함)

    특정 섹터의 상세 정보와 속한 종목 리스트를 조회합니다.

    Args:
        sector_code: 섹터코드

    Returns:
        섹터 상세 정보 + 종목 리스트
    '''
    try:
        result = await sector_service.get_sector_with_stocks(db, sector_code)

        if not result:
            raise HTTPException(status_code=404, detail=f"섹터를 찾을 수 없습니다: {sector_code}")

        return APIResponse(
            success=True,
            message="섹터 조회 성공",
            data=result.model_dump()
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="섹터 조회 실패",
            error=str(e)
        )


@router.get("/stock/{stock_code}/sectors")
async def get_stock_sectors(
        stock_code: str,
        db: AsyncSession = Depends(get_db)
):
    '''종목이 속한 섹터 리스트 조회

    특정 종목이 속한 모든 섹터를 조회합니다.

    Args:
        stock_code: 종목코드

    Returns:
        섹터 리스트
    '''
    try:
        sectors = await sector_service.get_stock_sectors(db, stock_code)

        return APIResponse(
            success=True,
            message=f"종목 섹터 조회 성공: {stock_code}",
            data={
                "stock_code": stock_code,
                "sectors": [s.model_dump() for s in sectors],
                "total_count": len(sectors)
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="종목 섹터 조회 실패",
            error=str(e)
        )


# ========== 섹터 관리 API (수동) ==========

@router.post("/create")
async def create_sector(
        sector_data: SectorCreate,
        db: AsyncSession = Depends(get_db)
):
    '''섹터 수동 생성

    키움 API 없이 직접 섹터를 생성합니다.

    Args:
        sector_data: 섹터 정보 (code, name, market, category, level, parent_id)

    Returns:
        생성된 섹터 정보
    '''
    try:
        repo = SectorRepository(db)

        # 중복 체크
        existing = await repo.get_sector_by_code(sector_data.code)
        if existing:
            raise HTTPException(status_code=400, detail=f"이미 존재하는 섹터 코드입니다: {sector_data.code}")

        # 섹터 생성
        sector = await repo.create_sector(sector_data)

        return APIResponse(
            success=True,
            message="섹터 생성 성공",
            data={
                "id": sector.id,
                "code": sector.code,
                "name": sector.name,
                "market": sector.market
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="섹터 생성 실패",
            error=str(e)
        )


@router.put("/{sector_id}")
async def update_sector(
        sector_id: int,
        sector_data: SectorUpdate,
        db: AsyncSession = Depends(get_db)
):
    '''섹터 정보 수정

    섹터의 이름, 시장, 카테고리 등을 수정합니다.

    Args:
        sector_id: 섹터 ID
        sector_data: 수정할 정보

    Returns:
        수정된 섹터 정보
    '''
    try:
        repo = SectorRepository(db)

        # 존재 확인
        existing = await repo.get_sector_by_id(sector_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"섹터를 찾을 수 없습니다: {sector_id}")

        # 수정
        updated_sector = await repo.update_sector(sector_id, sector_data)

        return APIResponse(
            success=True,
            message="섹터 수정 성공",
            data={
                "id": updated_sector.id,
                "code": updated_sector.code,
                "name": updated_sector.name,
                "market": updated_sector.market
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="섹터 수정 실패",
            error=str(e)
        )


@router.delete("/{sector_id}")
async def delete_sector(
        sector_id: int,
        db: AsyncSession = Depends(get_db)
):
    '''섹터 삭제

    섹터와 관련된 모든 종목 매핑도 함께 삭제됩니다.

    Args:
        sector_id: 섹터 ID

    Returns:
        삭제 결과
    '''
    try:
        repo = SectorRepository(db)

        # 존재 확인
        existing = await repo.get_sector_by_id(sector_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"섹터를 찾을 수 없습니다: {sector_id}")

        # 삭제
        success = await repo.delete_sector(sector_id)

        if success:
            return APIResponse(
                success=True,
                message=f"섹터 삭제 성공: {existing.name}",
                data={"deleted_id": sector_id}
            )
        else:
            return APIResponse(
                success=False,
                message="섹터 삭제 실패",
                error="알 수 없는 오류"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="섹터 삭제 실패",
            error=str(e)
        )


@router.post("/{sector_id}/stocks/{stock_code}")
async def add_stock_to_sector(
        sector_id: int,
        stock_code: str,
        db: AsyncSession = Depends(get_db)
):
    '''섹터에 종목 추가

    특정 섹터에 종목을 수동으로 추가합니다.

    Args:
        sector_id: 섹터 ID
        stock_code: 종목코드

    Returns:
        추가 결과
    '''
    try:
        repo = SectorRepository(db)

        # 섹터 존재 확인
        sector = await repo.get_sector_by_id(sector_id)
        if not sector:
            raise HTTPException(status_code=404, detail=f"섹터를 찾을 수 없습니다: {sector_id}")

        # 종목 추가
        await repo.add_stock_to_sector(stock_code, sector_id)

        return APIResponse(
            success=True,
            message=f"종목 추가 성공: {stock_code} → {sector.name}",
            data={
                "sector_id": sector_id,
                "stock_code": stock_code
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="종목 추가 실패",
            error=str(e)
        )


@router.delete("/{sector_id}/stocks/{stock_code}")
async def remove_stock_from_sector(
        sector_id: int,
        stock_code: str,
        db: AsyncSession = Depends(get_db)
):
    '''섹터에서 종목 제거

    특정 섹터에서 종목을 제거합니다.

    Args:
        sector_id: 섹터 ID
        stock_code: 종목코드

    Returns:
        제거 결과
    '''
    try:
        repo = SectorRepository(db)

        # 섹터 존재 확인
        sector = await repo.get_sector_by_id(sector_id)
        if not sector:
            raise HTTPException(status_code=404, detail=f"섹터를 찾을 수 없습니다: {sector_id}")

        # 종목 제거
        success = await repo.remove_stock_from_sector(stock_code, sector_id)

        if success:
            return APIResponse(
                success=True,
                message=f"종목 제거 성공: {stock_code} ← {sector.name}",
                data={
                    "sector_id": sector_id,
                    "stock_code": stock_code
                }
            )
        else:
            return APIResponse(
                success=False,
                message="종목 제거 실패 (매핑이 존재하지 않음)",
                error=f"{stock_code}가 섹터 {sector_id}에 속해있지 않습니다"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="종목 제거 실패",
            error=str(e)
        )


@router.post("/{sector_id}/stocks/bulk")
async def bulk_add_stocks_to_sector(
        sector_id: int,
        stock_codes: List[str] = Body(..., description="종목코드 리스트"),
        db: AsyncSession = Depends(get_db)
):
    '''섹터에 여러 종목 일괄 추가

    여러 종목을 한 번에 섹터에 추가합니다.

    Args:
        sector_id: 섹터 ID
        stock_codes: 종목코드 리스트

    Returns:
        추가 결과
    '''
    try:
        repo = SectorRepository(db)

        # 섹터 존재 확인
        sector = await repo.get_sector_by_id(sector_id)
        if not sector:
            raise HTTPException(status_code=404, detail=f"섹터를 찾을 수 없습니다: {sector_id}")

        # 일괄 추가
        await repo.bulk_add_stocks_to_sector(sector_id, stock_codes)

        return APIResponse(
            success=True,
            message=f"{len(stock_codes)}개 종목 일괄 추가 성공 → {sector.name}",
            data={
                "sector_id": sector_id,
                "added_count": len(stock_codes)
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return APIResponse(
            success=False,
            message="종목 일괄 추가 실패",
            error=str(e)
        )
