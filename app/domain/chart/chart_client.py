from typing import Optional

import httpx

from app.config import settings
from app.domain.chart.dto.response.chart_item import (
    MinuteChartItem, MinuteChartResponse,
    DayChartItem, DayChartResponse,
    WeekChartItem, WeekChartResponse,
    MonthChartItem, MonthChartResponse,
)


class ChartClient:

    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL
        self.url = f"{self.base_url}/api/dostk/chart"

    def _build_headers(self, access_token: str, api_id: str, cont_yn: Optional[str], next_key: Optional[str]) -> dict:
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "authorization": f"Bearer {access_token}",
            "api-id": api_id,
        }
        if cont_yn:
            headers["cont-yn"] = cont_yn
        if next_key:
            headers["next-key"] = next_key
        return headers

    async def get_minute_chart(
        self,
        access_token: str,
        stk_cd: str,
        tic_scope: str,
        upd_stkpc_tp: str,
        base_dt: Optional[str] = None,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MinuteChartResponse:
        """주식분봉차트조회요청 (ka10080)"""
        headers = self._build_headers(access_token, "ka10080", cont_yn, next_key)
        body = {
            "stk_cd": stk_cd,
            "tic_scope": tic_scope,
            "upd_stkpc_tp": upd_stkpc_tp,
        }
        if base_dt:
            body["base_dt"] = base_dt

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        return MinuteChartResponse(
            cont_yn=response.headers.get("cont-yn"),
            next_key=response.headers.get("next-key"),
            items=[
                MinuteChartItem(**item)
                for item in data.get("stk_min_pole_chart_qry", [])
            ],
        )

    async def get_day_chart(
        self,
        access_token: str,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> DayChartResponse:
        """주식일봉차트조회요청 (ka10081)"""
        headers = self._build_headers(access_token, "ka10081", cont_yn, next_key)
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        return DayChartResponse(
            cont_yn=response.headers.get("cont-yn"),
            next_key=response.headers.get("next-key"),
            items=[
                DayChartItem(**item)
                for item in data.get("stk_dt_pole_chart_qry", [])
            ],
        )

    async def get_week_chart(
        self,
        access_token: str,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> WeekChartResponse:
        """주식주봉차트조회요청 (ka10082)"""
        headers = self._build_headers(access_token, "ka10082", cont_yn, next_key)
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        return WeekChartResponse(
            cont_yn=response.headers.get("cont-yn"),
            next_key=response.headers.get("next-key"),
            items=[
                WeekChartItem(**item)
                for item in data.get("stk_stk_pole_chart_qry", [])
            ],
        )

    async def get_month_chart(
        self,
        access_token: str,
        stk_cd: str,
        base_dt: str,
        upd_stkpc_tp: str,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> MonthChartResponse:
        """주식월봉차트조회요청 (ka10083)"""
        headers = self._build_headers(access_token, "ka10083", cont_yn, next_key)
        body = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        return MonthChartResponse(
            cont_yn=response.headers.get("cont-yn"),
            next_key=response.headers.get("next-key"),
            items=[
                MonthChartItem(**item)
                for item in data.get("stk_mth_pole_chart_qry", [])
            ],
        )
