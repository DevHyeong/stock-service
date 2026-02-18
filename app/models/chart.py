from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, Index
from sqlalchemy.types import Numeric

from app.db import Base


class StockChartMinute(Base):
    """주식 분봉 차트 데이터 (ka10080)"""
    __tablename__ = "stock_chart_minute"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    stock_code = Column(String(32), nullable=False, index=True, comment="종목코드")
    cntr_tm = Column(String(14), nullable=False, comment="체결시간 (YYYYMMDDHHMMSS)")

    # OHLCV
    open_pric = Column(BigInteger, comment="시가")
    high_pric = Column(BigInteger, comment="고가")
    low_pric = Column(BigInteger, comment="저가")
    cur_prc = Column(BigInteger, comment="종가(현재가)")
    trde_qty = Column(BigInteger, comment="거래량")
    acc_trde_qty = Column(BigInteger, comment="누적거래량")

    # 전일대비
    pred_pre = Column(BigInteger, comment="전일대비")
    pred_pre_sig = Column(String(2), comment="전일대비부호")

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")

    __table_args__ = (
        Index('idx_chart_minute_unique', 'stock_code', 'cntr_tm', unique=True),
        Index('idx_chart_minute_code_tm', 'stock_code', 'cntr_tm'),
        {'comment': '주식 분봉 차트 데이터'},
    )

    def __repr__(self):
        return f"<StockChartMinute(code={self.stock_code}, tm={self.cntr_tm}, close={self.cur_prc})>"


class StockChartDaily(Base):
    """주식 일봉 차트 데이터 (ka10081)"""
    __tablename__ = "stock_chart_daily"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    stock_code = Column(String(32), nullable=False, index=True, comment="종목코드")
    dt = Column(String(8), nullable=False, comment="일자 (YYYYMMDD)")

    # OHLCV
    open_pric = Column(BigInteger, comment="시가")
    high_pric = Column(BigInteger, comment="고가")
    low_pric = Column(BigInteger, comment="저가")
    cur_prc = Column(BigInteger, comment="종가(현재가)")
    trde_qty = Column(BigInteger, comment="거래량")
    trde_prica = Column(BigInteger, comment="거래대금")

    # 전일대비
    pred_pre = Column(BigInteger, comment="전일대비")
    pred_pre_sig = Column(String(2), comment="전일대비부호")

    trde_tern_rt = Column(Numeric(10, 2), comment="거래회전율")

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")

    __table_args__ = (
        Index('idx_chart_daily_unique', 'stock_code', 'dt', unique=True),
        Index('idx_chart_daily_dt', 'dt'),
        {'comment': '주식 일봉 차트 데이터'},
    )

    def __repr__(self):
        return f"<StockChartDaily(code={self.stock_code}, dt={self.dt}, close={self.cur_prc})>"


class StockChartWeekly(Base):
    """주식 주봉 차트 데이터 (ka10082)"""
    __tablename__ = "stock_chart_weekly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    stock_code = Column(String(32), nullable=False, index=True, comment="종목코드")
    dt = Column(String(8), nullable=False, comment="주 시작일 (YYYYMMDD)")

    # OHLCV
    open_pric = Column(BigInteger, comment="시가")
    high_pric = Column(BigInteger, comment="고가")
    low_pric = Column(BigInteger, comment="저가")
    cur_prc = Column(BigInteger, comment="종가(현재가)")
    trde_qty = Column(BigInteger, comment="거래량")
    trde_prica = Column(BigInteger, comment="거래대금")

    # 전일대비
    pred_pre = Column(BigInteger, comment="전일대비")
    pred_pre_sig = Column(String(2), comment="전일대비부호")

    trde_tern_rt = Column(Numeric(10, 2), comment="거래회전율")

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")

    __table_args__ = (
        Index('idx_chart_weekly_unique', 'stock_code', 'dt', unique=True),
        Index('idx_chart_weekly_dt', 'dt'),
        {'comment': '주식 주봉 차트 데이터'},
    )

    def __repr__(self):
        return f"<StockChartWeekly(code={self.stock_code}, dt={self.dt}, close={self.cur_prc})>"


class StockChartMonthly(Base):
    """주식 월봉 차트 데이터 (ka10083)"""
    __tablename__ = "stock_chart_monthly"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    stock_code = Column(String(32), nullable=False, index=True, comment="종목코드")
    dt = Column(String(8), nullable=False, comment="월 시작일 (YYYYMMDD)")

    # OHLCV
    open_pric = Column(BigInteger, comment="시가")
    high_pric = Column(BigInteger, comment="고가")
    low_pric = Column(BigInteger, comment="저가")
    cur_prc = Column(BigInteger, comment="종가(현재가)")
    trde_qty = Column(BigInteger, comment="거래량")
    trde_prica = Column(BigInteger, comment="거래대금")

    # 전일대비
    pred_pre = Column(BigInteger, comment="전일대비")
    pred_pre_sig = Column(String(2), comment="전일대비부호")

    trde_tern_rt = Column(Numeric(10, 2), comment="거래회전율")

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")

    __table_args__ = (
        Index('idx_chart_monthly_unique', 'stock_code', 'dt', unique=True),
        Index('idx_chart_monthly_dt', 'dt'),
        {'comment': '주식 월봉 차트 데이터'},
    )

    def __repr__(self):
        return f"<StockChartMonthly(code={self.stock_code}, dt={self.dt}, close={self.cur_prc})>"
