from typing import List, Optional
from pydantic import BaseModel


class PriceLevel(BaseModel):
    """가격 레벨"""
    price: float
    touches: int  # 터치 횟수
    strength: str  # 강도: weak, medium, strong


class ResistanceSupportResponse(BaseModel):
    """저항/지지선 분석 응답"""
    stock_code: str
    timeframe: str  # day, week, month
    period: str  # 분석 기간 (예: 20260101-20260228)
    current_price: float

    resistance_levels: List[PriceLevel] = []  # 저항선 목록
    support_levels: List[PriceLevel] = []     # 지지선 목록

    nearest_resistance: Optional[float] = None  # 가장 가까운 저항선
    nearest_support: Optional[float] = None     # 가장 가까운 지지선

    analysis_summary: str  # 분석 요약


class VolumeProfileLevel(BaseModel):
    """거래량 프로파일 가격대"""
    price_range: str  # 가격 범위 (예: "50000-51000")
    volume: int
    percentage: float  # 전체 거래량 대비 비율


class VolumeProfileResponse(BaseModel):
    """거래량 프로파일 분석 응답"""
    stock_code: str
    timeframe: str
    period: str

    high_volume_levels: List[VolumeProfileLevel] = []  # 거래량 많은 가격대
    poc: Optional[float] = None  # Point of Control (최대 거래량 가격)
    value_area_high: Optional[float] = None  # 가치 영역 상단 (거래량 70%)
    value_area_low: Optional[float] = None   # 가치 영역 하단
