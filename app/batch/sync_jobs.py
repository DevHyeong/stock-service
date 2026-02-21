"""
배치 작업 Wrapper 함수

APScheduler는 동기 함수만 지원하므로,
각 Job 클래스를 asyncio.run()으로 실행하는 wrapper 함수를 제공합니다.
"""
import asyncio

from app.batch.jobs import (
    DailyChartSyncJob,
    MinuteChartSyncJob,
    WeeklyChartSyncJob,
    MonthlyChartSyncJob,
    TradingRankingSyncJob,
    InvestorDailyTradeSyncJob,
)


def run_sync_daily_chart_job():
    """일봉 차트 동기화 작업 실행"""
    job = DailyChartSyncJob()
    asyncio.run(job.run())


def run_sync_minute_chart_job():
    """분봉 차트 동기화 작업 실행"""
    job = MinuteChartSyncJob()
    asyncio.run(job.run())


def run_sync_weekly_chart_job():
    """주봉 차트 동기화 작업 실행"""
    job = WeeklyChartSyncJob()
    asyncio.run(job.run())


def run_sync_monthly_chart_job():
    """월봉 차트 동기화 작업 실행"""
    job = MonthlyChartSyncJob()
    asyncio.run(job.run())


def run_sync_trading_ranking_job():
    """거래대금 순위 동기화 작업 실행"""
    job = TradingRankingSyncJob()
    asyncio.run(job.run())


def run_sync_investor_daily_trade_job():
    """투자자별 일별 매매 동기화 작업 실행"""
    job = InvestorDailyTradeSyncJob()
    asyncio.run(job.run())
