from typing import Optional

from app.domain.chart.repositories.chart_repository import ChartRepository
from app.domain.chart.unit_of_work import ChartUnitOfWork
from app.domain.chart.dto.response.chart_item import (
    MinuteChartResponse,
    DayChartResponse,
    WeekChartResponse,
    MonthChartResponse,
)


class ChartService:
    def __init__(self, chart_repository: ChartRepository):
        self.chart_repository = chart_repository

    # ── POST: Kiwoom API → DB ─────────────────────────────────────────────────

    async def sync_minute_chart(
        self,
        stk_cd: str,
        tic_scope: str,
        upd_stkpc_tp: str,
        base_dt: Optional[str] = None,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MinuteChartResponse:
        """분봉 차트를 Kiwoom API에서 조회하고 DB에 저장 (ka10080)"""
        response = await self.chart_repository.get_minute_chart(
            stk_cd=stk_cd,
            tic_scope=tic_scope,
            upd_stkpc_tp=upd_stkpc_tp,
            base_dt=base_dt,
            cont_yn=cont_yn,
            next_key=next_key,
        )

        async with ChartUnitOfWork() as uow:
            await uow.chart_repo.bulk_upsert_minute(stk_cd, response.items)
            await uow.commit()

        return response

    async def sync_day_chart(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> DayChartResponse:
        """일봉 차트를 Kiwoom API에서 조회하고 DB에 저장 (ka10081)"""
        response = await self.chart_repository.get_day_chart(
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )

        async with ChartUnitOfWork() as uow:
            await uow.chart_repo.bulk_upsert_daily(stk_cd, response.items)
            await uow.commit()

        return response

    async def sync_week_chart(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> WeekChartResponse:
        """주봉 차트를 Kiwoom API에서 조회하고 DB에 저장 (ka10082)"""
        response = await self.chart_repository.get_week_chart(
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )

        async with ChartUnitOfWork() as uow:
            await uow.chart_repo.bulk_upsert_weekly(stk_cd, response.items)
            await uow.commit()

        return response

    async def sync_month_chart(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MonthChartResponse:
        """월봉 차트를 Kiwoom API에서 조회하고 DB에 저장 (ka10083)"""
        response = await self.chart_repository.get_month_chart(
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )

        async with ChartUnitOfWork() as uow:
            await uow.chart_repo.bulk_upsert_monthly(stk_cd, response.items)
            await uow.commit()

        return response

    # ── GET: DB 조회 ──────────────────────────────────────────────────────────

    async def get_minute_chart(self, stk_cd: str, date: str) -> MinuteChartResponse:
        """DB에서 분봉 차트 조회 (date: YYYYMMDD)"""
        async with ChartUnitOfWork() as uow:
            items = await uow.chart_repo.get_minute(stk_cd, date)
        return MinuteChartResponse(items=items)

    async def get_day_chart(self, stk_cd: str, start_dt: str, end_dt: str) -> DayChartResponse:
        """DB에서 일봉 차트 조회"""
        async with ChartUnitOfWork() as uow:
            items = await uow.chart_repo.get_daily(stk_cd, start_dt, end_dt)
        return DayChartResponse(items=items)

    async def get_week_chart(self, stk_cd: str, start_dt: str, end_dt: str) -> WeekChartResponse:
        """DB에서 주봉 차트 조회"""
        async with ChartUnitOfWork() as uow:
            items = await uow.chart_repo.get_weekly(stk_cd, start_dt, end_dt)
        return WeekChartResponse(items=items)

    async def get_month_chart(self, stk_cd: str, start_dt: str, end_dt: str) -> MonthChartResponse:
        """DB에서 월봉 차트 조회"""
        async with ChartUnitOfWork() as uow:
            items = await uow.chart_repo.get_monthly(stk_cd, start_dt, end_dt)
        return MonthChartResponse(items=items)
