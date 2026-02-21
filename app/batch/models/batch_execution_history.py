from sqlalchemy import Column, BigInteger, String, DateTime, Integer, Text
from app.db import Base


class BatchExecutionHistory(Base):
    __tablename__ = "batch_execution_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False, index=True)
    started_at = Column(DateTime, nullable=False, index=True)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)
    status = Column(String(20), nullable=False, index=True)
    record_count = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime)
