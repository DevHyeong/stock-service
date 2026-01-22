from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 기본 정보
    code = Column(String(32), unique=True, nullable=False, index=True, comment="종목코드")
    name = Column(String(256), nullable=False, comment="종목명")

    # 거래 정보
    list_count = Column(String(20), comment="상장주식수")
    audit_info = Column(String(100), comment="감리구분")
    reg_day = Column(String(8), comment="상장일(YYYYMMDD)")
    last_price = Column(String(20), comment="최종가격")
    state = Column(String(256), comment="종목상태")

    # 시장 정보
    market_code = Column(String(10), comment="시장코드(0:거래소,1:코스닥)")
    market_name = Column(String(50), comment="시장명")

    # 업종 정보
    up_name = Column(String(100), comment="업종명")
    up_size_name = Column(String(100), comment="업종규모명")

    # 기타 정보
    company_class_name = Column(String(100), comment="기업구분명")
    order_warning = Column(String(10), comment="주문경고")
    nxt_enable = Column(String(1), comment="익일매매가능여부(Y/N)")

    # 메타데이터
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    is_active = Column(Boolean, default=True, comment="활성화여부")

    def __repr__(self):
        return f"<Stock(code={self.code}, name={self.name}, market={self.market_name})>"
