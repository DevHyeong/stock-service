from typing import Optional

from app.common.auth_client import AuthClient
from app.domain.chart.chart_client import ChartClient
from app.domain.chart.dto.response.chart_item import (
    MinuteChartResponse,
    DayChartResponse,
    WeekChartResponse,
    MonthChartResponse,
)


class ChartRepository:
    def __init__(self, auth_client: AuthClient, chart_client: ChartClient):
        self.auth_client = auth_client
        self.chart_client = chart_client

    async def get_minute_chart(
        self,
        stk_cd: str,
        tic_scope: str,
        upd_stkpc_tp: str,
        base_dt: Optional[str] = None,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MinuteChartResponse:
        token = await self.auth_client.ensure_token()
        return await self.chart_client.get_minute_chart(
            access_token=token,
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
        token = await self.auth_client.ensure_token()
        return await self.chart_client.get_day_chart(
            access_token=token,
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
        token = await self.auth_client.ensure_token()
        return await self.chart_client.get_week_chart(
            access_token=token,
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
        token = await self.auth_client.ensure_token()
        return await self.chart_client.get_month_chart(
            access_token=token,
            stk_cd=stk_cd,
            base_dt=base_dt,
            upd_stkpc_tp=upd_stkpc_tp,
            cont_yn=cont_yn,
            next_key=next_key,
        )
