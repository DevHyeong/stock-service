from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from app.db import Base


class DataSyncSchedule(Base):
    __tablename__ = "data_sync_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)

    table_name = Column(String(100), nullable=False, unique=True)
    sync_type = Column(String(50), nullable=False)  # FULL, INCREMENTAL
    cron_expression = Column(String(50))
    interval_minutes = Column(Integer)

    last_sync_at = Column(DateTime)
    next_sync_at = Column(DateTime)
    last_sync_status = Column(String(20))  # SUCCESS, FAILED, RUNNING
    last_sync_count = Column(Integer, default=0)
    last_error_message = Column(Text)

    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
