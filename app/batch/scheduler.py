import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.batch.sync_jobs import (
    run_sync_daily_chart_job,
    run_sync_minute_chart_job,
    run_sync_weekly_chart_job,
    run_sync_monthly_chart_job,
    run_sync_trading_ranking_job,
    run_sync_investor_daily_trade_job,
)

logger = logging.getLogger(__name__)

# AsyncIOScheduler 생성
scheduler = AsyncIOScheduler()


def init_scheduler():
    """스케줄러 초기화 및 작업 등록"""

    # 일봉 차트 동기화: 매일 오전 7시 (장 시작 전)
    scheduler.add_job(
        run_sync_daily_chart_job,
        trigger=CronTrigger(hour=7, minute=0),
        id="sync_daily_chart",
        name="일봉 차트 동기화",
        replace_existing=True,
    )
    logger.info("일봉 차트 동기화 스케줄 등록: 매일 07:00")

    # 분봉 차트 동기화: 매일 오후 4시 (장 마감 후)
    scheduler.add_job(
        run_sync_minute_chart_job,
        trigger=CronTrigger(hour=16, minute=0),
        id="sync_minute_chart",
        name="분봉 차트 동기화",
        replace_existing=True,
    )
    logger.info("분봉 차트 동기화 스케줄 등록: 매일 16:00")

    # 주봉 차트 동기화: 매주 월요일 오전 8시
    scheduler.add_job(
        run_sync_weekly_chart_job,
        trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
        id="sync_weekly_chart",
        name="주봉 차트 동기화",
        replace_existing=True,
    )
    logger.info("주봉 차트 동기화 스케줄 등록: 매주 월요일 08:00")

    # 월봉 차트 동기화: 매월 1일 오전 9시
    scheduler.add_job(
        run_sync_monthly_chart_job,
        trigger=CronTrigger(day=1, hour=9, minute=0),
        id="sync_monthly_chart",
        name="월봉 차트 동기화",
        replace_existing=True,
    )
    logger.info("월봉 차트 동기화 스케줄 등록: 매월 1일 09:00")

    # 거래대금 순위 동기화: 매일 오후 4시 10분 (장 마감 후)
    scheduler.add_job(
        run_sync_trading_ranking_job,
        trigger=CronTrigger(hour=16, minute=10),
        id="sync_trading_ranking",
        name="거래대금 순위 동기화",
        replace_existing=True,
    )
    logger.info("거래대금 순위 동기화 스케줄 등록: 매일 16:10")

    # 투자자별 일별 매매 동기화: 매일 오후 5시 (장 마감 후, 데이터 집계 완료 시점)
    scheduler.add_job(
        run_sync_investor_daily_trade_job,
        trigger=CronTrigger(hour=17, minute=0),
        id="sync_investor_daily_trade",
        name="투자자별 일별 매매 동기화",
        replace_existing=True,
    )
    logger.info("투자자별 일별 매매 동기화 스케줄 등록: 매일 17:00")


def start_scheduler():
    """스케줄러 시작"""
    init_scheduler()
    scheduler.start()
    logger.info("배치 스케줄러 시작됨")


def shutdown_scheduler():
    """스케줄러 종료"""
    scheduler.shutdown()
    logger.info("배치 스케줄러 종료됨")
