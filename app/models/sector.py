from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base


class Sector(Base):
    '''섹터/업종 마스터 테이블'''
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 섹터 정보
    code = Column(String(50), unique=True, nullable=False, comment='섹터코드 (업종지수코드)')
    name = Column(String(100), nullable=False, comment='섹터명')

    # 분류 정보
    market = Column(String(20), comment='시장구분 (KOSPI/KOSDAQ/KRX)')
    category = Column(String(50), comment='대분류 (WICS 등)')
    level = Column(Integer, default=1, comment='분류레벨 (1:대분류, 2:중분류, 3:소분류)')
    parent_id = Column(Integer, ForeignKey('sectors.id', ondelete='SET NULL'), comment='상위 섹터 ID')

    # 통계 정보
    stock_count = Column(Integer, default=0, comment='속한 종목 수')

    # 메타데이터
    created_at = Column(DateTime, server_default=func.now(), comment='생성일시')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='수정일시')
    is_active = Column(Boolean, default=True, comment='활성화여부')

    # Relationships
    parent = relationship('Sector', remote_side=[id], backref='children')
    stock_sectors = relationship('StockSector', back_populates='sector', cascade='all, delete-orphan')


class StockSector(Base):
    '''종목-섹터 매핑 테이블'''
    __tablename__ = 'stock_sectors'

    id = Column(Integer, primary_key=True, autoincrement=True)

    stock_code = Column(String(32), nullable=False, comment='종목코드')
    sector_id = Column(Integer, ForeignKey('sectors.id', ondelete='CASCADE'), nullable=False, comment='섹터 ID')

    # 메타데이터
    created_at = Column(DateTime, server_default=func.now(), comment='생성일시')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='수정일시')

    # Relationships
    sector = relationship('Sector', back_populates='stock_sectors')
