from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SectorBase(BaseModel):
    '''섹터 기본 스키마'''
    code: str = Field(..., description="섹터코드")
    name: str = Field(..., description="섹터명")
    market: Optional[str] = Field(None, description="시장구분 (KOSPI/KOSDAQ/KRX)")
    category: Optional[str] = Field(None, description="대분류")
    level: int = Field(1, description="분류레벨")
    parent_id: Optional[int] = Field(None, description="상위 섹터 ID")


class SectorCreate(SectorBase):
    '''섹터 생성 스키마'''
    pass


class SectorUpdate(BaseModel):
    '''섹터 수정 스키마'''
    name: Optional[str] = None
    market: Optional[str] = None
    category: Optional[str] = None
    level: Optional[int] = None
    parent_id: Optional[int] = None
    stock_count: Optional[int] = None
    is_active: Optional[bool] = None


class SectorResponse(SectorBase):
    '''섹터 응답 스키마'''
    id: int
    stock_count: int = Field(default=0, description="속한 종목 수")
    is_active: bool = Field(default=True, description="활성화여부")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SectorWithStocksResponse(SectorResponse):
    '''종목 포함 섹터 응답 스키마'''
    stocks: List[dict] = Field(default_factory=list, description="속한 종목 리스트")


class StockSectorBase(BaseModel):
    '''종목-섹터 매핑 기본 스키마'''
    stock_code: str = Field(..., description="종목코드")
    sector_id: int = Field(..., description="섹터 ID")


class StockSectorCreate(StockSectorBase):
    '''종목-섹터 매핑 생성 스키마'''
    pass


class StockSectorResponse(StockSectorBase):
    '''종목-섹터 매핑 응답 스키마'''
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SectorListResponse(BaseModel):
    '''섹터 리스트 응답'''
    sectors: List[SectorResponse]
    total_count: int


class StockWithSectorsResponse(BaseModel):
    '''섹터 포함 종목 응답'''
    stock_code: str
    stock_name: Optional[str] = None
    sectors: List[SectorResponse]
