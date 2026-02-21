import logging
from abc import ABC, abstractmethod

from app.batch.schedule_manager import ScheduleManager

logger = logging.getLogger(__name__)


class BaseSyncJob(ABC):
    """배치 동기화 작업 추상 클래스 (템플릿 메서드 패턴)"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.history_id = None

    async def run(self) -> None:
        """배치 작업 실행 (템플릿 메서드)

        공통 로직:
        1. 활성화 여부 확인
        2. 히스토리 생성
        3. 동기화 시작 상태 업데이트
        4. 실제 작업 실행 (execute() 호출)
        5. 성공/실패 상태 업데이트
        """
        try:
            # 활성화 여부 확인
            if not await ScheduleManager.is_enabled(self.table_name):
                logger.info(f"[{self.table_name}] 스케줄이 비활성화되어 있습니다.")
                return

            # 히스토리 생성 및 동기화 시작
            self.history_id = await ScheduleManager.create_history(self.table_name)
            await ScheduleManager.update_sync_start(self.table_name)

            # 실제 동기화 작업 실행 (서브클래스에서 구현)
            count = await self.execute()

            # 동기화 완료
            await ScheduleManager.update_sync_success(self.table_name, count)
            await ScheduleManager.update_history_success(self.history_id, count)
            logger.info(f"[{self.table_name}] 동기화 완료: {count}건")

        except Exception as e:
            logger.exception(f"[{self.table_name}] 동기화 중 오류 발생")
            await ScheduleManager.update_sync_failed(self.table_name, str(e))
            if self.history_id:
                await ScheduleManager.update_history_failed(self.history_id, str(e))

    @abstractmethod
    async def execute(self) -> int:
        """실제 동기화 작업을 수행하고 처리된 레코드 수를 반환

        Returns:
            처리된 레코드 수
        """
        pass
