from typing import List

from sqlalchemy import func, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chart.dto.response.chart_item import (
    MinuteChartItem,
    DayChartItem,
    WeekChartItem,
    MonthChartItem,
)
from app.models.chart import (
    StockChartMinute,
    StockChartDaily,
    StockChartWeekly,
    StockChartMonthly,
)


def _to_int(value: str) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def _to_float(value: str):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class ChartDbRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Minute ────────────────────────────────────────────────────────────────

    async def bulk_upsert_minute(self, stock_code: str, items: List[MinuteChartItem]) -> int:
        if not items:
            return 0

        data = [
            {
                'stock_code': stock_code,
                'cntr_tm': item.cntr_tm,
                'open_pric': _to_int(item.open_pric),
                'high_pric': _to_int(item.high_pric),
                'low_pric': _to_int(item.low_pric),
                'cur_prc': _to_int(item.cur_prc),
                'trde_qty': _to_int(item.trde_qty),
                'acc_trde_qty': _to_int(item.acc_trde_qty),
                'pred_pre': _to_int(item.pred_pre),
                'pred_pre_sig': item.pred_pre_sig,
            }
            for item in items
        ]

        stmt = insert(StockChartMinute).values(data)
        stmt = stmt.on_duplicate_key_update(
            open_pric=stmt.inserted.open_pric,
            high_pric=stmt.inserted.high_pric,
            low_pric=stmt.inserted.low_pric,
            cur_prc=stmt.inserted.cur_prc,
            trde_qty=stmt.inserted.trde_qty,
            acc_trde_qty=stmt.inserted.acc_trde_qty,
            pred_pre=stmt.inserted.pred_pre,
            pred_pre_sig=stmt.inserted.pred_pre_sig,
            updated_at=func.now(),
        )
        await self.db.execute(stmt)
        return len(data)

    async def get_minute(self, stock_code: str, date: str) -> List[MinuteChartItem]:
        """date: YYYYMMDD — 해당 날짜의 모든 분봉 반환"""
        stmt = (
            select(StockChartMinute)
            .where(
                StockChartMinute.stock_code == stock_code,
                StockChartMinute.cntr_tm.like(f"{date}%"),
            )
            .order_by(StockChartMinute.cntr_tm)
        )
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        return [
            MinuteChartItem(
                cur_prc=str(row.cur_prc or 0),
                trde_qty=str(row.trde_qty or 0),
                cntr_tm=row.cntr_tm,
                open_pric=str(row.open_pric or 0),
                high_pric=str(row.high_pric or 0),
                low_pric=str(row.low_pric or 0),
                acc_trde_qty=str(row.acc_trde_qty or 0),
                pred_pre=str(row.pred_pre or 0),
                pred_pre_sig=row.pred_pre_sig or "",
            )
            for row in rows
        ]

    # ── Daily ─────────────────────────────────────────────────────────────────

    async def bulk_upsert_daily(self, stock_code: str, items: List[DayChartItem]) -> int:
        if not items:
            return 0

        data = [
            {
                'stock_code': stock_code,
                'dt': item.dt,
                'open_pric': _to_int(item.open_pric),
                'high_pric': _to_int(item.high_pric),
                'low_pric': _to_int(item.low_pric),
                'cur_prc': _to_int(item.cur_prc),
                'trde_qty': _to_int(item.trde_qty),
                'trde_prica': _to_int(item.trde_prica),
                'pred_pre': _to_int(item.pred_pre),
                'pred_pre_sig': item.pred_pre_sig,
                'trde_tern_rt': _to_float(item.trde_tern_rt),
            }
            for item in items
        ]

        stmt = insert(StockChartDaily).values(data)
        stmt = stmt.on_duplicate_key_update(
            open_pric=stmt.inserted.open_pric,
            high_pric=stmt.inserted.high_pric,
            low_pric=stmt.inserted.low_pric,
            cur_prc=stmt.inserted.cur_prc,
            trde_qty=stmt.inserted.trde_qty,
            trde_prica=stmt.inserted.trde_prica,
            pred_pre=stmt.inserted.pred_pre,
            pred_pre_sig=stmt.inserted.pred_pre_sig,
            trde_tern_rt=stmt.inserted.trde_tern_rt,
            updated_at=func.now(),
        )
        await self.db.execute(stmt)
        return len(data)

    async def get_daily(self, stock_code: str, start_dt: str, end_dt: str) -> List[DayChartItem]:
        stmt = (
            select(StockChartDaily)
            .where(
                StockChartDaily.stock_code == stock_code,
                StockChartDaily.dt.between(start_dt, end_dt),
            )
            .order_by(StockChartDaily.dt)
        )
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        return [
            DayChartItem(
                cur_prc=str(row.cur_prc or 0),
                trde_qty=str(row.trde_qty or 0),
                trde_prica=str(row.trde_prica or 0),
                dt=row.dt,
                open_pric=str(row.open_pric or 0),
                high_pric=str(row.high_pric or 0),
                low_pric=str(row.low_pric or 0),
                pred_pre=str(row.pred_pre or 0),
                pred_pre_sig=row.pred_pre_sig or "",
                trde_tern_rt=str(row.trde_tern_rt) if row.trde_tern_rt is not None else None,
            )
            for row in rows
        ]

    # ── Weekly ────────────────────────────────────────────────────────────────

    async def bulk_upsert_weekly(self, stock_code: str, items: List[WeekChartItem]) -> int:
        if not items:
            return 0

        data = [
            {
                'stock_code': stock_code,
                'dt': item.dt,
                'open_pric': _to_int(item.open_pric),
                'high_pric': _to_int(item.high_pric),
                'low_pric': _to_int(item.low_pric),
                'cur_prc': _to_int(item.cur_prc),
                'trde_qty': _to_int(item.trde_qty),
                'trde_prica': _to_int(item.trde_prica),
                'pred_pre': _to_int(item.pred_pre),
                'pred_pre_sig': item.pred_pre_sig,
                'trde_tern_rt': _to_float(item.trde_tern_rt),
            }
            for item in items
        ]

        stmt = insert(StockChartWeekly).values(data)
        stmt = stmt.on_duplicate_key_update(
            open_pric=stmt.inserted.open_pric,
            high_pric=stmt.inserted.high_pric,
            low_pric=stmt.inserted.low_pric,
            cur_prc=stmt.inserted.cur_prc,
            trde_qty=stmt.inserted.trde_qty,
            trde_prica=stmt.inserted.trde_prica,
            pred_pre=stmt.inserted.pred_pre,
            pred_pre_sig=stmt.inserted.pred_pre_sig,
            trde_tern_rt=stmt.inserted.trde_tern_rt,
            updated_at=func.now(),
        )
        await self.db.execute(stmt)
        return len(data)

    async def get_weekly(self, stock_code: str, start_dt: str, end_dt: str) -> List[WeekChartItem]:
        stmt = (
            select(StockChartWeekly)
            .where(
                StockChartWeekly.stock_code == stock_code,
                StockChartWeekly.dt.between(start_dt, end_dt),
            )
            .order_by(StockChartWeekly.dt)
        )
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        return [
            WeekChartItem(
                cur_prc=str(row.cur_prc or 0),
                trde_qty=str(row.trde_qty or 0),
                trde_prica=str(row.trde_prica or 0),
                dt=row.dt,
                open_pric=str(row.open_pric or 0),
                high_pric=str(row.high_pric or 0),
                low_pric=str(row.low_pric or 0),
                pred_pre=str(row.pred_pre or 0),
                pred_pre_sig=row.pred_pre_sig or "",
                trde_tern_rt=str(row.trde_tern_rt) if row.trde_tern_rt is not None else None,
            )
            for row in rows
        ]

    # ── Monthly ───────────────────────────────────────────────────────────────

    async def bulk_upsert_monthly(self, stock_code: str, items: List[MonthChartItem]) -> int:
        if not items:
            return 0

        data = [
            {
                'stock_code': stock_code,
                'dt': item.dt,
                'open_pric': _to_int(item.open_pric),
                'high_pric': _to_int(item.high_pric),
                'low_pric': _to_int(item.low_pric),
                'cur_prc': _to_int(item.cur_prc),
                'trde_qty': _to_int(item.trde_qty),
                'trde_prica': _to_int(item.trde_prica),
                'pred_pre': _to_int(item.pred_pre),
                'pred_pre_sig': item.pred_pre_sig,
                'trde_tern_rt': _to_float(item.trde_tern_rt),
            }
            for item in items
        ]

        stmt = insert(StockChartMonthly).values(data)
        stmt = stmt.on_duplicate_key_update(
            open_pric=stmt.inserted.open_pric,
            high_pric=stmt.inserted.high_pric,
            low_pric=stmt.inserted.low_pric,
            cur_prc=stmt.inserted.cur_prc,
            trde_qty=stmt.inserted.trde_qty,
            trde_prica=stmt.inserted.trde_prica,
            pred_pre=stmt.inserted.pred_pre,
            pred_pre_sig=stmt.inserted.pred_pre_sig,
            trde_tern_rt=stmt.inserted.trde_tern_rt,
            updated_at=func.now(),
        )
        await self.db.execute(stmt)
        return len(data)

    async def get_monthly(self, stock_code: str, start_dt: str, end_dt: str) -> List[MonthChartItem]:
        stmt = (
            select(StockChartMonthly)
            .where(
                StockChartMonthly.stock_code == stock_code,
                StockChartMonthly.dt.between(start_dt, end_dt),
            )
            .order_by(StockChartMonthly.dt)
        )
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        return [
            MonthChartItem(
                cur_prc=str(row.cur_prc or 0),
                trde_qty=str(row.trde_qty or 0),
                trde_prica=str(row.trde_prica or 0),
                dt=row.dt,
                open_pric=str(row.open_pric or 0),
                high_pric=str(row.high_pric or 0),
                low_pric=str(row.low_pric or 0),
                pred_pre=str(row.pred_pre or 0),
                pred_pre_sig=row.pred_pre_sig or "",
                trde_tern_rt=str(row.trde_tern_rt) if row.trde_tern_rt is not None else None,
            )
            for row in rows
        ]
