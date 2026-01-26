from typing import Optional, List
from pydantic import BaseModel


class TradeRankItem(BaseModel):
    """거래대금상위 종목 정보"""
    stk_cd: str  # 종목코드
    now_rank: str  # 현재순위
    pred_rank: str  # 전일순위
    stk_nm: str  # 종목명
    cur_prc: str  # 현재가
    pred_pre_sig: str  # 전일대비기호
    pred_pre: str  # 전일대비
    flu_rt: str  # 등락률
    sel_bid: str  # 매도호가
    buy_bid: str  # 매수호가
    now_trde_qty: str  # 현재거래량
    pred_trde_qty: str  # 전일거래량
    trde_prica: str  # 거래대금

class TradeRankResponse(BaseModel):
    """ka10058 응답 모델"""
    cont_yn: Optional[str] = None  # 연속조회여부
    next_key: Optional[str] = None  # 연속조회키
    trde_prica_upper: List[TradeRankItem] = []  # 거래대금상위 목록
