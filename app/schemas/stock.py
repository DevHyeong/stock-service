from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ForeignTradingRequest(BaseModel):
    '''외국인 매매동향 조회 요청'''
    stock_code: str = Field(..., min_length=6, max_length=6, description="종목코드 (6자리)")
    date: Optional[str] = Field(None, pattern=r'^\d{8}$', description="조회일자 (YYYYMMDD)")
    direction: str = Field(default="0", description="정렬구분 (0:순매수상위, 1:순매도상위)")


class ForeignTradingItem(BaseModel):
    '''외국인 매매동향 항목'''
    dt: str = Field(..., description="거래일자 (YYYYMMDD)")
    close_pric: str = Field(..., description="종가")
    pred_pre: str = Field(..., description="전일대비")
    trde_qty: str = Field(..., description="거래량")
    chg_qty: str = Field(..., description="순매수량")
    poss_stkcnt: str = Field(..., description="보유주식수")
    wght: str = Field(..., description="보유비중")
    gain_pos_stkcnt: str = Field(..., description="상장주식수")
    frgnr_limit: str = Field(..., description="외국인한도")
    frgnr_limit_irds: str = Field(..., description="외국인한도소진률")
    limit_exh_rt: str = Field(..., description="한도소진률")


class ForeignTradingResponse(BaseModel):
    '''외국인 매매동향 응답'''
    items: list[ForeignTradingItem]
    total_count: int

class StockItem(BaseModel):
    code: str = Field(..., description="종목코드")
    name: str = Field(..., description="종목명")
    listCount: str = Field(..., description="상장주식수(문자열, 0 패딩 유지)")
    auditInfo: Optional[str] = Field(None, description="감리/감시 정보")
    regDay: Optional[str] = Field(None, description="등록일자 (YYYYMMDD)")
    lastPrice: str = Field(..., description="현재가(문자열)")
    state: Optional[str] = Field(None, description="상태")
    marketCode: Optional[str] = Field(None, description="시장코드")
    marketName: Optional[str] = Field(None, description="시장명")
    upName: Optional[str] = Field(None, description="upName")
    upSizeName: Optional[str] = Field(None, description="upSizeName")
    companyClassName: Optional[str] = Field(None, description="companyClassName")
    orderWarning: Optional[str] = Field(None, description="orderWarning")
    nxtEnable: Optional[str] = Field(None, description="nxtEnable (Y/N)")
