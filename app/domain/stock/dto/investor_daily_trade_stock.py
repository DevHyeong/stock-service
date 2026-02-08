from typing import List

from pydantic import BaseModel

class InvestorDailyTradeStock(BaseModel):
    stk_cd: str  # 종목코드
    stk_nm: str  # 종목명
    netslmt_qty: str  # 순매도수량
    netslmt_amt: str  # 순매도금액
    prsm_avg_pric: str  # 추정평균가
    cur_prc: str  # 현재가
    pre_sig: str  # 대비기호
    pred_pre: str  # 전일대비
    avg_pric_pre: str  # 평균가대비
    pre_rt: str  # 대비율
    dt_trde_qty: str  # 기간거래량 # 기간거래량

class InvestorDailyTradeResponse(BaseModel):
    invsr_daly_trde_stk: List[InvestorDailyTradeStock]
    return_code: int
    return_msg: str

class InvestorDailyTradeStockRequest(BaseModel):
    strt_dt: str  # 시작일자 (YYYYMMDD)
    end_dt: str  # 종료일자 (YYYYMMDD)
    trde_tp: str  # 매매구분 (1: 순매도, 2: 순매수)
    mrkt_tp: str  # 시장구분 (001: 코스피, 101: 코스닥)
    invsr_tp: str  # 투자자구분 (8000: 개인, 9000: 외국인, ...)
    stex_tp: str  # 거래소구분 (1: KRX, 2: NXT, 3: 통합)