from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.sector import Sector, StockSector
from app.schemas.sector import SectorCreate, SectorUpdate, StockSectorCreate
from app.core.logger import logger


class SectorRepository:
    '''섹터 Repository'''

    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_sector(self, sector_data: SectorCreate) -> Sector:
        '''섹터 생성'''
        sector = Sector(**sector_data.model_dump())
        self.db.add(sector)
        await self.db.commit()
        await self.db.refresh(sector)
        logger.info(f"섹터 생성: {sector.code} - {sector.name}")
        return sector


    async def get_sector_by_code(self, code: str) -> Optional[Sector]:
        '''코드로 섹터 조회'''
        query = select(Sector).where(Sector.code == code)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def get_sector_by_id(self, sector_id: int) -> Optional[Sector]:
        '''ID로 섹터 조회'''
        query = select(Sector).where(Sector.id == sector_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def get_all_sectors(
        self,
        market: Optional[str] = None,
        category: Optional[str] = None,
        is_active: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Sector]:
        '''섹터 리스트 조회'''
        query = select(Sector).where(Sector.is_active == is_active)

        if market:
            query = query.where(Sector.market == market)

        if category:
            query = query.where(Sector.category == category)

        query = query.offset(skip).limit(limit).order_by(Sector.code)

        result = await self.db.execute(query)
        return result.scalars().all()


    async def count_sectors(
        self,
        market: Optional[str] = None,
        category: Optional[str] = None,
        is_active: bool = True
    ) -> int:
        '''섹터 개수 조회'''
        query = select(func.count(Sector.id)).where(Sector.is_active == is_active)

        if market:
            query = query.where(Sector.market == market)

        if category:
            query = query.where(Sector.category == category)

        result = await self.db.execute(query)
        return result.scalar_one()


    async def update_sector(self, sector_id: int, sector_data: SectorUpdate) -> Optional[Sector]:
        '''섹터 수정'''
        update_data = sector_data.model_dump(exclude_unset=True)

        if not update_data:
            return await self.get_sector_by_id(sector_id)

        query = (
            update(Sector)
            .where(Sector.id == sector_id)
            .values(**update_data)
            .returning(Sector)
        )

        result = await self.db.execute(query)
        await self.db.commit()

        updated_sector = result.scalar_one_or_none()
        if updated_sector:
            logger.info(f"섹터 수정: {sector_id}")

        return updated_sector


    async def upsert_sector(self, sector_data: SectorCreate) -> Sector:
        '''섹터 생성 또는 수정 (코드 기준)'''
        existing = await self.get_sector_by_code(sector_data.code)

        if existing:
            # 업데이트
            update_data = SectorUpdate(**sector_data.model_dump(exclude={'code'}))
            return await self.update_sector(existing.id, update_data)
        else:
            # 생성
            return await self.create_sector(sector_data)


    async def delete_sector(self, sector_id: int) -> bool:
        '''섹터 삭제'''
        query = delete(Sector).where(Sector.id == sector_id)
        result = await self.db.execute(query)
        await self.db.commit()

        if result.rowcount > 0:
            logger.info(f"섹터 삭제: {sector_id}")
            return True

        return False


    async def add_stock_to_sector(self, stock_code: str, sector_id: int) -> StockSector:
        '''섹터에 종목 추가'''
        # 이미 존재하는지 확인
        query = select(StockSector).where(
            StockSector.stock_code == stock_code,
            StockSector.sector_id == sector_id
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            return existing

        # 새로 추가
        stock_sector = StockSector(stock_code=stock_code, sector_id=sector_id)
        self.db.add(stock_sector)

        # 섹터의 종목 수 업데이트
        await self.increment_sector_stock_count(sector_id)

        await self.db.commit()
        await self.db.refresh(stock_sector)

        logger.info(f"섹터에 종목 추가: {stock_code} -> {sector_id}")
        return stock_sector


    async def remove_stock_from_sector(self, stock_code: str, sector_id: int) -> bool:
        '''섹터에서 종목 제거'''
        query = delete(StockSector).where(
            StockSector.stock_code == stock_code,
            StockSector.sector_id == sector_id
        )
        result = await self.db.execute(query)

        if result.rowcount > 0:
            # 섹터의 종목 수 업데이트
            await self.decrement_sector_stock_count(sector_id)
            await self.db.commit()
            logger.info(f"섹터에서 종목 제거: {stock_code} <- {sector_id}")
            return True

        await self.db.commit()
        return False


    async def get_stocks_by_sector(self, sector_id: int) -> List[str]:
        '''섹터에 속한 종목 코드 리스트'''
        query = select(StockSector.stock_code).where(StockSector.sector_id == sector_id)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_sectors_by_stock(self, stock_code: str) -> List[Sector]:
        '''종목이 속한 섹터 리스트'''
        query = (
            select(Sector)
            .join(StockSector, Sector.id == StockSector.sector_id)
            .where(StockSector.stock_code == stock_code)
        )
        result = await self.db.execute(query)
        return result.scalars().all()


    async def increment_sector_stock_count(self, sector_id: int):
        '''섹터 종목 수 증가'''
        query = (
            update(Sector)
            .where(Sector.id == sector_id)
            .values(stock_count=Sector.stock_count + 1)
        )
        await self.db.execute(query)


    async def decrement_sector_stock_count(self, sector_id: int):
        '''섹터 종목 수 감소'''
        query = (
            update(Sector)
            .where(Sector.id == sector_id)
            .values(stock_count=func.greatest(Sector.stock_count - 1, 0))
        )
        await self.db.execute(query)


    async def bulk_add_stocks_to_sector(self, sector_id: int, stock_codes: List[str]):
        '''섹터에 여러 종목 일괄 추가'''
        # 기존 종목 조회
        existing_query = select(StockSector.stock_code).where(
            StockSector.sector_id == sector_id
        )
        result = await self.db.execute(existing_query)
        existing_codes = set(result.scalars().all())

        # 새로운 종목만 추가
        new_codes = [code for code in stock_codes if code not in existing_codes]

        if new_codes:
            stock_sectors = [
                StockSector(stock_code=code, sector_id=sector_id)
                for code in new_codes
            ]
            self.db.add_all(stock_sectors)

            # 종목 수 업데이트
            query = (
                update(Sector)
                .where(Sector.id == sector_id)
                .values(stock_count=Sector.stock_count + len(new_codes))
            )
            await self.db.execute(query)

            await self.db.commit()
            logger.info(f"섹터에 종목 일괄 추가: {sector_id}, {len(new_codes)}개")


    async def clear_sector_stocks(self, sector_id: int):
        '''섹터의 모든 종목 제거'''
        query = delete(StockSector).where(StockSector.sector_id == sector_id)
        await self.db.execute(query)

        # 종목 수 0으로 초기화
        update_query = (
            update(Sector)
            .where(Sector.id == sector_id)
            .values(stock_count=0)
        )
        await self.db.execute(update_query)

        await self.db.commit()
        logger.info(f"섹터 종목 전체 제거: {sector_id}")
