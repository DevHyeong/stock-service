from pydantic import BaseModel, Field, ConfigDict
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


# 체결정보 관련
class ExecutionInfoItem(BaseModel):
    '''체결정보 항목'''
    tm: str = Field(..., description="시간 (HHMMSS)")
    cur_prc: str = Field(..., description="현재가")
    pred_pre: str = Field(..., description="전일대비")
    pre_rt: str = Field(..., description="전일대비율")
    pri_sel_bid_unit: str = Field(..., description="최우선매도호가")
    pri_buy_bid_unit: str = Field(..., description="최우선매수호가")
    cntr_trde_qty: str = Field(..., description="체결거래량")
    sign: str = Field(..., description="대비기호")
    acc_trde_qty: str = Field(..., description="누적거래량")
    acc_trde_prica: str = Field(..., description="누적거래대금")
    cntr_str: str = Field(..., description="체결강도")
    stex_tp: str = Field(..., description="거래소구분")


class ExecutionInfoResponse(BaseModel):
    '''체결정보 응답'''
    items: list[ExecutionInfoItem]
    return_code: int
    return_msg: str


# 호가 관련
class BidAskItem(BaseModel):
    '''호가 항목'''
    bid_req_base_tm: Optional[str] = Field(None, description="호가조회기준시각")
    bid_rem_qty_10: Optional[str] = Field(None, description="매도호가잔량10")
    bid_unit_10: Optional[str] = Field(None, description="매도호가10")
    bid_unit_9: Optional[str] = Field(None, description="매도호가9")
    bid_rem_qty_9: Optional[str] = Field(None, description="매도호가잔량9")
    bid_unit_8: Optional[str] = Field(None, description="매도호가8")
    bid_rem_qty_8: Optional[str] = Field(None, description="매도호가잔량8")
    bid_unit_7: Optional[str] = Field(None, description="매도호가7")
    bid_rem_qty_7: Optional[str] = Field(None, description="매도호가잔량7")
    bid_unit_6: Optional[str] = Field(None, description="매도호가6")
    bid_rem_qty_6: Optional[str] = Field(None, description="매도호가잔량6")
    bid_unit_5: Optional[str] = Field(None, description="매도호가5")
    bid_rem_qty_5: Optional[str] = Field(None, description="매도호가잔량5")
    bid_unit_4: Optional[str] = Field(None, description="매도호가4")
    bid_rem_qty_4: Optional[str] = Field(None, description="매도호가잔량4")
    bid_unit_3: Optional[str] = Field(None, description="매도호가3")
    bid_rem_qty_3: Optional[str] = Field(None, description="매도호가잔량3")
    bid_unit_2: Optional[str] = Field(None, description="매도호가2")
    bid_rem_qty_2: Optional[str] = Field(None, description="매도호가잔량2")
    bid_unit_1: Optional[str] = Field(None, description="매도호가1")
    bid_rem_qty_1: Optional[str] = Field(None, description="매도호가잔량1")
    ask_unit_1: Optional[str] = Field(None, description="매수호가1")
    ask_rem_qty_1: Optional[str] = Field(None, description="매수호가잔량1")
    ask_unit_2: Optional[str] = Field(None, description="매수호가2")
    ask_rem_qty_2: Optional[str] = Field(None, description="매수호가잔량2")
    ask_unit_3: Optional[str] = Field(None, description="매수호가3")
    ask_rem_qty_3: Optional[str] = Field(None, description="매수호가잔량3")
    ask_unit_4: Optional[str] = Field(None, description="매수호가4")
    ask_rem_qty_4: Optional[str] = Field(None, description="매수호가잔량4")
    ask_unit_5: Optional[str] = Field(None, description="매수호가5")
    ask_rem_qty_5: Optional[str] = Field(None, description="매수호가잔량5")
    ask_unit_6: Optional[str] = Field(None, description="매수호가6")
    ask_rem_qty_6: Optional[str] = Field(None, description="매수호가잔량6")
    ask_unit_7: Optional[str] = Field(None, description="매수호가7")
    ask_rem_qty_7: Optional[str] = Field(None, description="매수호가잔량7")
    ask_unit_8: Optional[str] = Field(None, description="매수호가8")
    ask_rem_qty_8: Optional[str] = Field(None, description="매수호가잔량8")
    ask_unit_9: Optional[str] = Field(None, description="매수호가9")
    ask_rem_qty_9: Optional[str] = Field(None, description="매수호가잔량9")
    ask_unit_10: Optional[str] = Field(None, description="매수호가10")
    ask_rem_qty_10: Optional[str] = Field(None, description="매수호가잔량10")


class BidAskResponse(BaseModel):
    '''호가 응답'''
    data: Optional[BidAskItem] = None
    return_code: int
    return_msg: str


# 차트 관련 (공통)
class TickChartItem(BaseModel):
    '''틱차트 항목'''
    cur_prc: str = Field(..., description="현재가")
    trde_qty: str = Field(..., description="거래량")
    cntr_tm: str = Field(..., description="체결시간")
    open_pric: str = Field(..., description="시가")
    high_pric: str = Field(..., description="고가")
    low_pric: str = Field(..., description="저가")
    pred_pre: str = Field(..., description="전일대비")
    pred_pre_sig: str = Field(..., description="전일대비부호")


class MinuteChartItem(BaseModel):
    '''분봉차트 항목'''
    cur_prc: str = Field(..., description="현재가")
    trde_qty: str = Field(..., description="거래량")
    cntr_tm: str = Field(..., description="체결시간")
    open_pric: str = Field(..., description="시가")
    high_pric: str = Field(..., description="고가")
    low_pric: str = Field(..., description="저가")
    acc_trde_qty: str = Field(..., description="누적거래량")
    pred_pre: str = Field(..., description="전일대비")
    pred_pre_sig: str = Field(..., description="전일대비부호")


class DayChartItem(BaseModel):
    '''일봉차트 항목'''
    cur_prc: str = Field(..., description="현재가")
    trde_qty: str = Field(..., description="거래량")
    trde_prica: str = Field(..., description="거래대금")
    dt: str = Field(..., description="일자")
    open_pric: str = Field(..., description="시가")
    high_pric: str = Field(..., description="고가")
    low_pric: str = Field(..., description="저가")
    pred_pre: str = Field(..., description="전일대비")
    pred_pre_sig: str = Field(..., description="전일대비부호")
    trde_tern_rt: Optional[str] = Field(None, description="거래회전율")


class WeekChartItem(BaseModel):
    '''주봉차트 항목'''
    cur_prc: str = Field(..., description="현재가")
    trde_qty: str = Field(..., description="거래량")
    trde_prica: str = Field(..., description="거래대금")
    dt: str = Field(..., description="일자")
    open_pric: str = Field(..., description="시가")
    high_pric: str = Field(..., description="고가")
    low_pric: str = Field(..., description="저가")
    pred_pre: str = Field(..., description="전일대비")
    pred_pre_sig: str = Field(..., description="전일대비부호")
    trde_tern_rt: Optional[str] = Field(None, description="거래회전율")


class MonthChartItem(BaseModel):
    '''월봉차트 항목'''
    cur_prc: str = Field(..., description="현재가")
    trde_qty: str = Field(..., description="거래량")
    trde_prica: str = Field(..., description="거래대금")
    dt: str = Field(..., description="일자")
    open_pric: str = Field(..., description="시가")
    high_pric: str = Field(..., description="고가")
    low_pric: str = Field(..., description="저가")
    pred_pre: str = Field(..., description="전일대비")
    pred_pre_sig: str = Field(..., description="전일대비부호")
    trde_tern_rt: Optional[str] = Field(None, description="거래회전율")


class ChartResponse(BaseModel):
    '''차트 응답 (공통)'''
    items: list
    return_code: int
    return_msg: str


# DB 조회용 Stock 응답 스키마
class StockResponse(BaseModel):
    '''DB에서 조회한 종목 정보'''
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str = Field(..., description="종목코드")
    name: str = Field(..., description="종목명")
    list_count: Optional[str] = Field(None, description="상장주식수")
    audit_info: Optional[str] = Field(None, description="감리구분")
    reg_day: Optional[str] = Field(None, description="상장일(YYYYMMDD)")
    last_price: Optional[str] = Field(None, description="최종가격")
    state: Optional[str] = Field(None, description="종목상태")
    market_code: Optional[str] = Field(None, description="시장코드(0:코스피,10:코스닥)")
    market_name: Optional[str] = Field(None, description="시장명")
    up_name: Optional[str] = Field(None, description="업종명")
    up_size_name: Optional[str] = Field(None, description="업종규모명")
    company_class_name: Optional[str] = Field(None, description="기업구분명")
    order_warning: Optional[str] = Field(None, description="주문경고")
    nxt_enable: Optional[str] = Field(None, description="익일매매가능여부(Y/N)")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")
    is_active: bool = Field(..., description="활성화여부")


class StockListResponse(BaseModel):
    '''종목 리스트 응답'''
    stocks: list[StockResponse]
    total: int = Field(..., description="전체 종목 수")
    skip: int = Field(..., description="건너뛴 개수")
    limit: int = Field(..., description="조회한 개수")
