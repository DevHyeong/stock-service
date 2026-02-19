from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime

from app.db import Base


class StockBasicInfo(Base):
    """주식 기본 정보 (ka10001)"""
    __tablename__ = "stock_basic_info"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 종목 기본
    stock_code = Column(String(32), nullable=False, unique=True, index=True, comment="종목코드")
    stock_name = Column(String(256), comment="종목명")
    setl_mm = Column(String(20), comment="결산월")
    fav = Column(String(20), comment="액면가")
    fav_unit = Column(String(20), comment="액면가단위")
    cap = Column(String(20), comment="자본금")
    flo_stk = Column(String(20), comment="상장주식")
    dstr_stk = Column(String(20), comment="유통주식")
    dstr_rt = Column(String(20), comment="유통비율")
    crd_rt = Column(String(20), comment="신용비율")

    # 시가총액
    mac = Column(String(30), comment="시가총액")
    mac_wght = Column(String(20), comment="시가총액비중")
    for_exh_rt = Column(String(20), comment="외인소진률")
    repl_pric = Column(String(20), comment="대용가")

    # 현재가 / 시세
    cur_prc = Column(String(20), comment="현재가")
    pre_sig = Column(String(5), comment="대비기호")
    pred_pre = Column(String(20), comment="전일대비")
    flu_rt = Column(String(20), comment="등락율")
    trde_qty = Column(String(20), comment="거래량")
    trde_pre = Column(String(20), comment="거래대비")
    open_pric = Column(String(20), comment="시가")
    high_pric = Column(String(20), comment="고가")
    low_pric = Column(String(20), comment="저가")
    upl_pric = Column(String(20), comment="상한가")
    lst_pric = Column(String(20), comment="하한가")
    base_pric = Column(String(20), comment="기준가")
    exp_cntr_pric = Column(String(20), comment="예상체결가")
    exp_cntr_qty = Column(String(20), comment="예상체결수량")

    # 연중 최고/최저
    oyr_hgst = Column(String(20), comment="연중최고")
    oyr_lwst = Column(String(20), comment="연중최저")

    # 250일 최고/최저
    hgst_250 = Column(String(20), comment="250일 최고가")
    hgst_250_pric_dt = Column(String(8), comment="250일 최고가일")
    hgst_250_pric_pre_rt = Column(String(20), comment="250일 최고가대비율")
    lwst_250 = Column(String(20), comment="250일 최저가")
    lwst_250_pric_dt = Column(String(8), comment="250일 최저가일")
    lwst_250_pric_pre_rt = Column(String(20), comment="250일 최저가대비율")

    # 재무 지표
    per = Column(String(20), comment="PER")
    eps = Column(String(20), comment="EPS")
    roe = Column(String(20), comment="ROE")
    pbr = Column(String(20), comment="PBR")
    ev = Column(String(20), comment="EV")
    bps = Column(String(20), comment="BPS")
    sale_amt = Column(String(20), comment="매출액")
    bus_pro = Column(String(20), comment="영업이익")
    cup_nga = Column(String(20), comment="당기순이익")

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
