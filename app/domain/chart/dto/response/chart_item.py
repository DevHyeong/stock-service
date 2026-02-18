from typing import Optional, List
from pydantic import BaseModel


class MinuteChartItem(BaseModel):
    """분봉 차트 항목"""
    cur_prc: str       # 현재가
    trde_qty: str      # 거래량
    cntr_tm: str       # 체결시간
    open_pric: str     # 시가
    high_pric: str     # 고가
    low_pric: str      # 저가
    acc_trde_qty: str  # 누적거래량
    pred_pre: str      # 전일대비
    pred_pre_sig: str  # 전일대비부호


class DayChartItem(BaseModel):
    """일봉 차트 항목"""
    cur_prc: str               # 현재가
    trde_qty: str              # 거래량
    trde_prica: str            # 거래대금
    dt: str                    # 일자
    open_pric: str             # 시가
    high_pric: str             # 고가
    low_pric: str              # 저가
    pred_pre: str              # 전일대비
    pred_pre_sig: str          # 전일대비부호
    trde_tern_rt: Optional[str] = None  # 거래회전율


class WeekChartItem(BaseModel):
    """주봉 차트 항목"""
    cur_prc: str               # 현재가
    trde_qty: str              # 거래량
    trde_prica: str            # 거래대금
    dt: str                    # 일자
    open_pric: str             # 시가
    high_pric: str             # 고가
    low_pric: str              # 저가
    pred_pre: str              # 전일대비
    pred_pre_sig: str          # 전일대비부호
    trde_tern_rt: Optional[str] = None  # 거래회전율


class MonthChartItem(BaseModel):
    """월봉 차트 항목"""
    cur_prc: str               # 현재가
    trde_qty: str              # 거래량
    trde_prica: str            # 거래대금
    dt: str                    # 일자
    open_pric: str             # 시가
    high_pric: str             # 고가
    low_pric: str              # 저가
    pred_pre: str              # 전일대비
    pred_pre_sig: str          # 전일대비부호
    trde_tern_rt: Optional[str] = None  # 거래회전율


class MinuteChartResponse(BaseModel):
    """분봉 차트 응답"""
    cont_yn: Optional[str] = None
    next_key: Optional[str] = None
    items: List[MinuteChartItem] = []


class DayChartResponse(BaseModel):
    """일봉 차트 응답"""
    cont_yn: Optional[str] = None
    next_key: Optional[str] = None
    items: List[DayChartItem] = []


class WeekChartResponse(BaseModel):
    """주봉 차트 응답"""
    cont_yn: Optional[str] = None
    next_key: Optional[str] = None
    items: List[WeekChartItem] = []


class MonthChartResponse(BaseModel):
    """월봉 차트 응답"""
    cont_yn: Optional[str] = None
    next_key: Optional[str] = None
    items: List[MonthChartItem] = []
