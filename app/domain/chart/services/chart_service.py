from typing import Optional

from app.domain.chart.repositories.chart_repository import ChartRepository
from app.domain.chart.dto.response.chart_item import (
    MinuteChartResponse,
    DayChartResponse,
    WeekChartResponse,
    MonthChartResponse,
)


class ChartService:
    def __init__(self, chart_repository: ChartRepository):
        self.chart_repository = chart_repository

    async def get_minute_chart(
        self,
        stk_cd: str,
        tic_scope: str,
        upd_stkpc_tp: str,
        base_dt: Optional[str] = None,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MinuteChartResponse:
        """분봉 차트 조회 (ka10080)"""
        return await self.chart_repository.get_minute_chart(
            stk_cd=stk_cd,
            tic_scope=tic_scope,
            upd_stkpc_tp=upd_stkpc_tp,
            base_dt=base_dt,
            cont_yn=cont_yn,
            next_key=next_key,
        )

    async def get_day_chart(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> DayChartResponse:
        """일봉 차트 조회 (ka10081)"""
        return await self.chart_repository.get_day_chart(
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )

    async def get_week_chart(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> WeekChartResponse:
        """주봉 차트 조회 (ka10082)"""
        return await self.chart_repository.get_week_chart(
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )

    async def get_month_chart(
        self,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MonthChartResponse:
        """월봉 차트 조회 (ka10083)"""
        return await self.chart_repository.get_month_chart(
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )
