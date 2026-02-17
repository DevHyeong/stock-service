from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class StockTradingDailyResponse(BaseModel):
    """일별 거래 정보 응답"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    stock_code: str = Field(..., description="종목코드")
    stock_name: str = Field(..., description="종목명")
    trade_date: date = Field(..., description="거래일자")

    # 가격 정보
    current_price: Optional[Decimal] = Field(None, description="현재가")
    change_amount: Optional[Decimal] = Field(None, description="전일대비")
    change_rate: Optional[Decimal] = Field(None, description="등락률")

    # 거래 정보
    trading_amount: Optional[int] = Field(None, description="거래대금")
    trading_volume: Optional[int] = Field(None, description="거래량")
    previous_trading_volume: Optional[int] = Field(None, description="전일거래량")

    # 호가 정보
    sell_bid: Optional[Decimal] = Field(None, description="매도호가")
    buy_bid: Optional[Decimal] = Field(None, description="매수호가")

    # 순위 정보
    current_rank: Optional[int] = Field(None, description="현재순위")
    previous_rank: Optional[int] = Field(None, description="전일순위")

    created_at: datetime
    updated_at: datetime


class TradingSyncRequest(BaseModel):
    """거래 정보 동기화 요청"""
    trade_date: Optional[date] = Field(None, description="거래일자 (없으면 오늘)")
    limit: int = Field(100, ge=1, le=500, description="상위 N개만 저장 (기본 100개)")


class TradingSyncResponse(BaseModel):
    """거래 정보 동기화 응답"""
    trade_date: date = Field(..., description="거래일자")
    synced_count: int = Field(..., description="저장된 종목 수")
    total_trading_amount: Optional[int] = Field(None, description="총 거래대금")


class TradingRankingResponse(BaseModel):
    """거래대금 순위 응답"""
    trade_date: date = Field(..., description="거래일자")
    rankings: list[StockTradingDailyResponse]
    total_count: int = Field(..., description="전체 개수")


class StockTradingHistoryResponse(BaseModel):
    """종목별 거래 히스토리 응답"""
    stock_code: str = Field(..., description="종목코드")
    stock_name: str = Field(..., description="종목명")
    history: list[StockTradingDailyResponse]
    total_count: int = Field(..., description="전체 개수")
