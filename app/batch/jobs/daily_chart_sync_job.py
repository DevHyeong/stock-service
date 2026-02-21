import logging
from datetime import datetime, timedelta

from app.batch.jobs.base_sync_job import BaseSyncJob
from app.containers import Container

logger = logging.getLogger(__name__)


class DailyChartSyncJob(BaseSyncJob):
    """일봉 차트 동기화 작업"""

    def __init__(self):
        super().__init__("chart_daily")

    async def execute(self) -> int:
        # 어제 날짜 기준으로 동기화
        base_dt = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

        # Container에서 ChartService 가져오기
        container = Container()
        chart_service = container.chart_service()

        # 배치 동기화 실행
        result = await chart_service.batch_sync_day_chart(
            base_dt=base_dt,
            upd_stkpc_tp="1",
            delay=0.5,
        )

        logger.info(f"[{self.table_name}] 성공 {result.success}건, 실패 {result.failed}건")
        return result.success
