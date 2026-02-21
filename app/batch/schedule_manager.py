import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.batch.models.data_sync_schedule import DataSyncSchedule
from app.batch.models.batch_execution_history import BatchExecutionHistory
from app.db import get_session

logger = logging.getLogger(__name__)


class ScheduleManager:
    """데이터 동기화 스케줄 관리"""

    @staticmethod
    async def get_schedule(table_name: str) -> Optional[DataSyncSchedule]:
        """스케줄 정보 조회"""
        async for session in get_session():
            stmt = select(DataSyncSchedule).where(DataSyncSchedule.table_name == table_name)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @staticmethod
    async def create_history(table_name: str) -> int:
        """배치 실행 히스토리 생성 (시작 기록)"""
        async for session in get_session():
            stmt = insert(BatchExecutionHistory).values(
                table_name=table_name,
                started_at=datetime.now(),
                status="RUNNING",
                created_at=datetime.now(),
            )
            result = await session.execute(stmt)
            await session.commit()
            history_id = result.lastrowid
            logger.info(f"[{table_name}] 히스토리 생성: ID={history_id}")
            return history_id

    @staticmethod
    async def update_history_success(history_id: int, count: int) -> None:
        """배치 실행 히스토리 업데이트 (성공)"""
        async for session in get_session():
            stmt = select(BatchExecutionHistory).where(BatchExecutionHistory.id == history_id)
            result = await session.execute(stmt)
            history = result.scalar_one_or_none()

            if history:
                completed_at = datetime.now()
                duration = int((completed_at - history.started_at).total_seconds())

                update_stmt = (
                    update(BatchExecutionHistory)
                    .where(BatchExecutionHistory.id == history_id)
                    .values(
                        completed_at=completed_at,
                        duration_seconds=duration,
                        status="SUCCESS",
                        record_count=count,
                    )
                )
                await session.execute(update_stmt)
                await session.commit()
                logger.info(f"[히스토리 ID={history_id}] 성공 기록: {count}건, {duration}초 소요")

    @staticmethod
    async def update_history_failed(history_id: int, error_message: str) -> None:
        """배치 실행 히스토리 업데이트 (실패)"""
        async for session in get_session():
            stmt = select(BatchExecutionHistory).where(BatchExecutionHistory.id == history_id)
            result = await session.execute(stmt)
            history = result.scalar_one_or_none()

            if history:
                completed_at = datetime.now()
                duration = int((completed_at - history.started_at).total_seconds())

                update_stmt = (
                    update(BatchExecutionHistory)
                    .where(BatchExecutionHistory.id == history_id)
                    .values(
                        completed_at=completed_at,
                        duration_seconds=duration,
                        status="FAILED",
                        error_message=error_message,
                    )
                )
                await session.execute(update_stmt)
                await session.commit()
                logger.error(f"[히스토리 ID={history_id}] 실패 기록: {error_message}, {duration}초 소요")

    @staticmethod
    async def update_sync_start(table_name: str) -> None:
        """동기화 시작 상태 업데이트"""
        async for session in get_session():
            stmt = (
                update(DataSyncSchedule)
                .where(DataSyncSchedule.table_name == table_name)
                .values(
                    last_sync_status="RUNNING",
                    last_sync_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            )
            await session.execute(stmt)
            await session.commit()
            logger.info(f"[{table_name}] 동기화 시작")

    @staticmethod
    async def update_sync_success(table_name: str, count: int) -> None:
        """동기화 성공 상태 업데이트"""
        async for session in get_session():
            stmt = (
                update(DataSyncSchedule)
                .where(DataSyncSchedule.table_name == table_name)
                .values(
                    last_sync_status="SUCCESS",
                    last_sync_count=count,
                    last_error_message=None,
                    updated_at=datetime.now(),
                )
            )
            await session.execute(stmt)
            await session.commit()
            logger.info(f"[{table_name}] 동기화 성공: {count}건")

    @staticmethod
    async def update_sync_failed(table_name: str, error_message: str) -> None:
        """동기화 실패 상태 업데이트"""
        async for session in get_session():
            stmt = (
                update(DataSyncSchedule)
                .where(DataSyncSchedule.table_name == table_name)
                .values(
                    last_sync_status="FAILED",
                    last_error_message=error_message,
                    updated_at=datetime.now(),
                )
            )
            await session.execute(stmt)
            await session.commit()
            logger.error(f"[{table_name}] 동기화 실패: {error_message}")

    @staticmethod
    async def is_enabled(table_name: str) -> bool:
        """스케줄 활성화 여부 확인"""
        schedule = await ScheduleManager.get_schedule(table_name)
        return schedule.is_enabled if schedule else False
