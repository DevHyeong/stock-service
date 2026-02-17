from sqlalchemy import Column, BigInteger, String, Date, Integer, DateTime, Index
from sqlalchemy.types import Numeric
from datetime import datetime, date
from app.db import Base


class StockTradingDaily(Base):
    """일별 종목 거래 정보"""
    __tablename__ = "stock_trading_daily"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 기본 정보
    stock_code = Column(String(32), nullable=False, index=True, comment="종목코드")
    stock_name = Column(String(256), nullable=False, comment="종목명")
    trade_date = Column(Date, nullable=False, index=True, comment="거래일자")

    # 가격 정보
    current_price = Column(Numeric(15, 2), comment="현재가")
    change_amount = Column(Numeric(15, 2), comment="전일대비")
    change_rate = Column(Numeric(10, 2), comment="등락률")

    # 거래 정보
    trading_amount = Column(BigInteger, comment="거래대금")
    trading_volume = Column(BigInteger, comment="거래량")
    previous_trading_volume = Column(BigInteger, comment="전일거래량")

    # 호가 정보
    sell_bid = Column(Numeric(15, 2), comment="매도호가")
    buy_bid = Column(Numeric(15, 2), comment="매수호가")

    # 순위 정보
    current_rank = Column(Integer, comment="현재순위")
    previous_rank = Column(Integer, comment="전일순위")

    # 메타데이터
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")

    # 복합 유니크 인덱스
    __table_args__ = (
        Index('idx_stock_date', 'stock_code', 'trade_date', unique=True),
    )

    def __repr__(self):
        return f"<StockTradingDaily(code={self.stock_code}, name={self.stock_name}, date={self.trade_date}, rank={self.current_rank})>"
