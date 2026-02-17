from sqlalchemy import Column, BigInteger, String, DateTime, Index
from datetime import datetime
from app.db import Base


class InvestorDailyTrade(Base):
    """투자자별 일별 매매 종목 정보"""
    __tablename__ = "investor_daily_trade"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 요청 파라미터 (컨텍스트)
    start_date = Column(String(8), nullable=False, comment="시작일자(YYYYMMDD)")
    end_date = Column(String(8), nullable=False, comment="종료일자(YYYYMMDD)")
    trade_type = Column(String(2), nullable=False, comment="매매구분(1:순매도,2:순매수)")
    market_type = Column(String(10), nullable=False, comment="시장구분(001:코스피,101:코스닥)")
    investor_type = Column(String(10), nullable=False, comment="투자자구분(8000:개인,9000:외국인...)")
    exchange_type = Column(String(2), nullable=False, comment="거래소구분(1:KRX,2:NXT,3:통합)")

    # 종목 정보
    stock_code = Column(String(32), nullable=False, index=True, comment="종목코드")
    stock_name = Column(String(256), nullable=False, comment="종목명")

    # 거래 데이터
    net_sell_qty = Column(String(30), comment="순매도수량")
    net_sell_amt = Column(String(30), comment="순매도금액")
    est_avg_price = Column(String(30), comment="추정평균가")
    current_price = Column(String(30), comment="현재가")
    change_sign = Column(String(5), comment="대비기호")
    day_change = Column(String(30), comment="전일대비")
    avg_price_change = Column(String(30), comment="평균가대비")
    change_rate = Column(String(20), comment="대비율")
    period_trade_volume = Column(String(30), comment="기간거래량")

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")

    __table_args__ = (
        Index(
            'idx_investor_trade_unique',
            'stock_code', 'end_date', 'investor_type', 'market_type', 'trade_type',
            unique=True
        ),
    )

    def __repr__(self):
        return f"<InvestorDailyTrade(code={self.stock_code}, end={self.end_date}, investor={self.investor_type})>"
