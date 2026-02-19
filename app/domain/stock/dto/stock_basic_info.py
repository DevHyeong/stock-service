from pydantic import BaseModel, ConfigDict, Field


class StockBasicInfoRequest(BaseModel):
    stk_cd: str  # 종목코드


class StockBasicInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # 종목 기본
    stk_cd: str = ""
    stk_nm: str = ""
    setl_mm: str = ""       # 결산월
    fav: str = ""           # 액면가
    fav_unit: str = ""      # 액면가단위
    cap: str = ""           # 자본금
    flo_stk: str = ""       # 상장주식
    dstr_stk: str = ""      # 유통주식
    dstr_rt: str = ""       # 유통비율
    crd_rt: str = ""        # 신용비율

    # 시가총액
    mac: str = ""           # 시가총액
    mac_wght: str = ""      # 시가총액비중
    for_exh_rt: str = ""    # 외인소진률
    repl_pric: str = ""     # 대용가

    # 현재가 / 시세
    cur_prc: str = ""       # 현재가
    pre_sig: str = ""       # 대비기호
    pred_pre: str = ""      # 전일대비
    flu_rt: str = ""        # 등락율
    trde_qty: str = ""      # 거래량
    trde_pre: str = ""      # 거래대비
    open_pric: str = ""     # 시가
    high_pric: str = ""     # 고가
    low_pric: str = ""      # 저가
    upl_pric: str = ""      # 상한가
    lst_pric: str = ""      # 하한가
    base_pric: str = ""     # 기준가
    exp_cntr_pric: str = "" # 예상체결가
    exp_cntr_qty: str = ""  # 예상체결수량

    # 연중 최고/최저
    oyr_hgst: str = ""      # 연중최고
    oyr_lwst: str = ""      # 연중최저

    # 250일 최고/최저
    hgst_250: str = Field(default="", alias="250hgst")
    hgst_250_pric_dt: str = Field(default="", alias="250hgst_pric_dt")
    hgst_250_pric_pre_rt: str = Field(default="", alias="250hgst_pric_pre_rt")
    lwst_250: str = Field(default="", alias="250lwst")
    lwst_250_pric_dt: str = Field(default="", alias="250lwst_pric_dt")
    lwst_250_pric_pre_rt: str = Field(default="", alias="250lwst_pric_pre_rt")

    # 재무 지표
    per: str = ""
    eps: str = ""
    roe: str = ""
    pbr: str = ""
    ev: str = ""
    bps: str = ""
    sale_amt: str = ""      # 매출액
    bus_pro: str = ""       # 영업이익
    cup_nga: str = ""       # 당기순이익


class StockBasicInfoResponse(StockBasicInfo):
    return_code: int = 0
    return_msg: str = ""
