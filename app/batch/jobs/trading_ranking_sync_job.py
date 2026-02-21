import logging
from datetime import date

from app.batch.jobs.base_sync_job import BaseSyncJob
from app.common.auth_client import AuthClient
from app.db import get_session
from app.domain.rank.enums.mang_stk_incls import MangStkIncls
from app.domain.rank.enums.market_type import MarketType
from app.domain.rank.rank_client import RankClient
from app.domain.rank.repositories.rank_repository import RankRepository
from app.domain.rank.services.rank_service import RankService
from app.repositories.trading_repository import TradingRepository
from app.services.trading_service import TradingService

logger = logging.getLogger(__name__)


class TradingRankingSyncJob(BaseSyncJob):
    """거래대금 순위 동기화 작업"""

    def __init__(self):
        super().__init__("trading_ranking")

    async def execute(self) -> int:
        # 오늘 날짜 기준으로 동기화
        trade_date = date.today()

        # 의존성 주입 (DB 세션 필요)
        async for session in get_session():
            auth_client = AuthClient()
            rank_client = RankClient()
            rank_repository = RankRepository(auth_client, rank_client)
            rank_service = RankService(rank_repository)
            trading_repo = TradingRepository(session)
            trading_service = TradingService(trading_repo, rank_service)

            # 거래대금 순위 동기화 실행
            result = await trading_service.sync_trading_data(
                trade_date=trade_date,
                limit=100,
                market_type=MarketType.ALL,
                include_managed=MangStkIncls.EXCLUDE,
            )

            return result.synced_count
