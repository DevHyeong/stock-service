import logging
from datetime import datetime, timedelta

from app.batch.jobs.base_sync_job import BaseSyncJob
from app.containers import Container
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStockRequest

logger = logging.getLogger(__name__)


class InvestorDailyTradeSyncJob(BaseSyncJob):
    """투자자별 일별 매매 동기화 작업"""

    def __init__(self):
        super().__init__("investor_daily_trade")

    async def execute(self) -> int:
        # 오늘 날짜 기준으로 동기화 (최근 5일)
        end_dt = datetime.now().strftime("%Y%m%d")
        start_dt = (datetime.now() - timedelta(days=5)).strftime("%Y%m%d")

        # Container에서 StockService 가져오기
        container = Container()
        stock_service = container.stock_service()

        # 투자자별 일별 매매 동기화 실행 (모든 조합)
        result = await stock_service.sync_investor_daily_trade_stock(
            investorDailyTradeStockRequest=InvestorDailyTradeStockRequest(
                strt_dt=start_dt,
                end_dt=end_dt,
                trde_tp=None,  # 전체 (순매도 + 순매수)
                mrkt_tp=None,  # 전체 (코스피 + 코스닥)
                invsr_tp=None,  # 전체 투자자 타입
                stex_tp=None,  # 전체 거래소
            )
        )

        return len(result)
