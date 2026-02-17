from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.domain.sector.repositories.sector_repository import SectorRepository
from app.schemas.sector import (
    SectorResponse,
    SectorListResponse, SectorWithStocksResponse
)


class SectorService:
    '''섹터 서비스'''

    async def get_all_sectors(
        self,
        db: AsyncSession,
        market: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> SectorListResponse:
        '''섹터 리스트 조회'''
        repo = SectorRepository(db)

        sectors = await repo.get_all_sectors(
            market=market,
            category=category,
            is_active=True,
            skip=skip,
            limit=limit
        )

        total_count = await repo.count_sectors(
            market=market,
            category=category,
            is_active=True
        )

        return SectorListResponse(
            sectors=[SectorResponse.model_validate(s) for s in sectors],
            total_count=total_count
        )


    async def get_sector_with_stocks(
        self,
        db: AsyncSession,
        sector_code: str
    ) -> Optional[SectorWithStocksResponse]:
        '''섹터와 속한 종목 조회'''
        repo = SectorRepository(db)

        sector = await repo.get_sector_by_code(sector_code)
        if not sector:
            return None

        # 종목 코드 리스트 조회
        stock_codes = await repo.get_stocks_by_sector(sector.id)

        # 종목 정보는 코드만 반환 (상세 정보는 별도 API 호출)
        stocks = [{"code": code} for code in stock_codes]

        sector_dict = SectorResponse.model_validate(sector).model_dump()
        sector_dict['stocks'] = stocks

        return SectorWithStocksResponse(**sector_dict)


    async def get_stock_sectors(
        self,
        db: AsyncSession,
        stock_code: str
    ) -> List[SectorResponse]:
        '''종목이 속한 섹터 리스트 조회'''
        repo = SectorRepository(db)

        sectors = await repo.get_sectors_by_stock(stock_code)

        return [SectorResponse.model_validate(s) for s in sectors]


# 싱글톤 인스턴스
sector_service = SectorService()
