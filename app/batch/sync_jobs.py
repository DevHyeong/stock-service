import asyncio
import logging
from datetime import datetime, timedelta, date

from app.batch.schedule_manager import ScheduleManager
from app.containers import Container
from app.domain.chart.services.chart_service import ChartService
from app.domain.rank.services.rank_service import RankService
from app.domain.rank.repositories.rank_repository import RankRepository
from app.domain.rank.rank_client import RankClient
from app.domain.rank.enums.market_type import MarketType
from app.domain.rank.enums.mang_stk_incls import MangStkIncls
from app.common.auth_client import AuthClient
from app.repositories.trading_repository import TradingRepository
from app.services.trading_service import TradingService
from app.domain.stock.services.stock_service import StockService
from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStockRequest
from app.db import get_session

logger = logging.getLogger(__name__)


async def sync_daily_chart_job():
    """일봉 차트 동기화 작업 (매일 오전 7시)"""
    table_name = "chart_daily"
    history_id = None

    try:
        # 활성화 여부 확인
        if not await ScheduleManager.is_enabled(table_name):
            logger.info(f"[{table_name}] 스케줄이 비활성화되어 있습니다.")
            return

        # 히스토리 생성 및 동기화 시작
        history_id = await ScheduleManager.create_history(table_name)
        await ScheduleManager.update_sync_start(table_name)

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

        # 동기화 완료
        await ScheduleManager.update_sync_success(table_name, result.success)
        await ScheduleManager.update_history_success(history_id, result.success)
        logger.info(f"[{table_name}] 일봉 차트 동기화 완료: 성공 {result.success}건, 실패 {result.failed}건")

    except Exception as e:
        logger.exception(f"[{table_name}] 일봉 차트 동기화 중 오류 발생")
        await ScheduleManager.update_sync_failed(table_name, str(e))
        if history_id:
            await ScheduleManager.update_history_failed(history_id, str(e))


async def sync_minute_chart_job():
    """분봉 차트 동기화 작업 (매일 오후 4시)"""
    table_name = "chart_minute"
    history_id = None

    try:
        # 활성화 여부 확인
        if not await ScheduleManager.is_enabled(table_name):
            logger.info(f"[{table_name}] 스케줄이 비활성화되어 있습니다.")
            return

        # 히스토리 생성 및 동기화 시작
        history_id = await ScheduleManager.create_history(table_name)
        await ScheduleManager.update_sync_start(table_name)

        # 오늘 날짜 기준으로 동기화
        base_dt = datetime.now().strftime("%Y%m%d")

        # Container에서 ChartService 가져오기
        container = Container()
        chart_service = container.chart_service()

        # 배치 동기화 실행 (1분봉)
        result = await chart_service.batch_sync_minute_chart(
            base_dt=base_dt,
            tic_scope="1",
            upd_stkpc_tp="1",
            delay=0.5,
        )

        # 동기화 완료
        await ScheduleManager.update_sync_success(table_name, result.success)
        await ScheduleManager.update_history_success(history_id, result.success)
        logger.info(f"[{table_name}] 분봉 차트 동기화 완료: 성공 {result.success}건, 실패 {result.failed}건")

    except Exception as e:
        logger.exception(f"[{table_name}] 분봉 차트 동기화 중 오류 발생")
        await ScheduleManager.update_sync_failed(table_name, str(e))
        if history_id:
            await ScheduleManager.update_history_failed(history_id, str(e))


async def sync_weekly_chart_job():
    """주봉 차트 동기화 작업 (매주 월요일 오전 8시)"""
    table_name = "chart_weekly"
    history_id = None

    try:
        # 활성화 여부 확인
        if not await ScheduleManager.is_enabled(table_name):
            logger.info(f"[{table_name}] 스케줄이 비활성화되어 있습니다.")
            return

        # 히스토리 생성 및 동기화 시작
        history_id = await ScheduleManager.create_history(table_name)
        await ScheduleManager.update_sync_start(table_name)

        # 지난주 금요일 날짜 기준으로 동기화
        base_dt = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")

        # Container에서 ChartService 가져오기
        container = Container()
        chart_service = container.chart_service()

        # 배치 동기화 실행
        result = await chart_service.batch_sync_week_chart(
            base_dt=base_dt,
            upd_stkpc_tp="1",
            delay=0.5,
        )

        # 동기화 완료
        await ScheduleManager.update_sync_success(table_name, result.success)
        await ScheduleManager.update_history_success(history_id, result.success)
        logger.info(f"[{table_name}] 주봉 차트 동기화 완료: 성공 {result.success}건, 실패 {result.failed}건")

    except Exception as e:
        logger.exception(f"[{table_name}] 주봉 차트 동기화 중 오류 발생")
        await ScheduleManager.update_sync_failed(table_name, str(e))
        if history_id:
            await ScheduleManager.update_history_failed(history_id, str(e))


async def sync_monthly_chart_job():
    """월봉 차트 동기화 작업 (매월 1일 오전 9시)"""
    table_name = "chart_monthly"
    history_id = None

    try:
        # 활성화 여부 확인
        if not await ScheduleManager.is_enabled(table_name):
            logger.info(f"[{table_name}] 스케줄이 비활성화되어 있습니다.")
            return

        # 히스토리 생성 및 동기화 시작
        history_id = await ScheduleManager.create_history(table_name)
        await ScheduleManager.update_sync_start(table_name)

        # 지난달 마지막 날 기준으로 동기화
        today = datetime.now()
        last_month = today.replace(day=1) - timedelta(days=1)
        base_dt = last_month.strftime("%Y%m%d")

        # Container에서 ChartService 가져오기
        container = Container()
        chart_service = container.chart_service()

        # 배치 동기화 실행
        result = await chart_service.batch_sync_month_chart(
            base_dt=base_dt,
            upd_stkpc_tp="1",
            delay=0.5,
        )

        # 동기화 완료
        await ScheduleManager.update_sync_success(table_name, result.success)
        await ScheduleManager.update_history_success(history_id, result.success)
        logger.info(f"[{table_name}] 월봉 차트 동기화 완료: 성공 {result.success}건, 실패 {result.failed}건")

    except Exception as e:
        logger.exception(f"[{table_name}] 월봉 차트 동기화 중 오류 발생")
        await ScheduleManager.update_sync_failed(table_name, str(e))
        if history_id:
            await ScheduleManager.update_history_failed(history_id, str(e))


async def sync_trading_ranking_job():
    """거래대금 순위 동기화 작업 (매일 오후 4시)"""
    table_name = "trading_ranking"
    history_id = None

    try:
        # 활성화 여부 확인
        if not await ScheduleManager.is_enabled(table_name):
            logger.info(f"[{table_name}] 스케줄이 비활성화되어 있습니다.")
            return

        # 히스토리 생성 및 동기화 시작
        history_id = await ScheduleManager.create_history(table_name)
        await ScheduleManager.update_sync_start(table_name)

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

            # 동기화 완료
            await ScheduleManager.update_sync_success(table_name, result.synced_count)
            await ScheduleManager.update_history_success(history_id, result.synced_count)
            logger.info(f"[{table_name}] 거래대금 순위 동기화 완료: {result.synced_count}건")
            break  # 첫 번째 세션만 사용

    except Exception as e:
        logger.exception(f"[{table_name}] 거래대금 순위 동기화 중 오류 발생")
        await ScheduleManager.update_sync_failed(table_name, str(e))
        if history_id:
            await ScheduleManager.update_history_failed(history_id, str(e))


async def sync_investor_daily_trade_job():
    """투자자별 일별 매매 동기화 작업 (매일 오후 5시)"""
    table_name = "investor_daily_trade"
    history_id = None

    try:
        # 활성화 여부 확인
        if not await ScheduleManager.is_enabled(table_name):
            logger.info(f"[{table_name}] 스케줄이 비활성화되어 있습니다.")
            return

        # 히스토리 생성 및 동기화 시작
        history_id = await ScheduleManager.create_history(table_name)
        await ScheduleManager.update_sync_start(table_name)

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

        # 동기화 완료
        await ScheduleManager.update_sync_success(table_name, len(result))
        await ScheduleManager.update_history_success(history_id, len(result))
        logger.info(f"[{table_name}] 투자자별 일별 매매 동기화 완료: {len(result)}건")

    except Exception as e:
        logger.exception(f"[{table_name}] 투자자별 일별 매매 동기화 중 오류 발생")
        await ScheduleManager.update_sync_failed(table_name, str(e))
        if history_id:
            await ScheduleManager.update_history_failed(history_id, str(e))


# 동기 wrapper 함수들 (APScheduler는 동기 함수만 지원)
def run_sync_daily_chart_job():
    """일봉 차트 동기화 작업 실행"""
    asyncio.run(sync_daily_chart_job())


def run_sync_minute_chart_job():
    """분봉 차트 동기화 작업 실행"""
    asyncio.run(sync_minute_chart_job())


def run_sync_weekly_chart_job():
    """주봉 차트 동기화 작업 실행"""
    asyncio.run(sync_weekly_chart_job())


def run_sync_monthly_chart_job():
    """월봉 차트 동기화 작업 실행"""
    asyncio.run(sync_monthly_chart_job())


def run_sync_trading_ranking_job():
    """거래대금 순위 동기화 작업 실행"""
    asyncio.run(sync_trading_ranking_job())


def run_sync_investor_daily_trade_job():
    """투자자별 일별 매매 동기화 작업 실행"""
    asyncio.run(sync_investor_daily_trade_job())
