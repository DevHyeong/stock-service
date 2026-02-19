from typing import List

from sqlalchemy import func, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.stock.dto.investor_daily_trade_stock import InvestorDailyTradeStock, InvestorDailyTradeStockRequest
from app.models.investor_daily_trade import InvestorDailyTrade


class InvestorDailyTradeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_upsert(
        self,
        trades: List[InvestorDailyTradeStock],
        request: InvestorDailyTradeStockRequest
    ) -> int:
        if not trades:
            return 0

        data = [
            {
                'start_date': request.strt_dt,
                'end_date': request.end_dt,
                'trade_type': request.trde_tp or "",
                'market_type': request.mrkt_tp or "",
                'investor_type': request.invsr_tp or "",
                'exchange_type': request.stex_tp or "",
                'stock_code': t.stk_cd,
                'stock_name': t.stk_nm,
                'net_sell_qty': t.netslmt_qty,
                'net_sell_amt': t.netslmt_amt,
                'est_avg_price': t.prsm_avg_pric,
                'current_price': t.cur_prc,
                'change_sign': t.pre_sig,
                'day_change': t.pred_pre,
                'avg_price_change': t.avg_pric_pre,
                'change_rate': t.pre_rt,
                'period_trade_volume': t.dt_trde_qty,
            }
            for t in trades
        ]

        stmt = insert(InvestorDailyTrade).values(data)
        stmt = stmt.on_duplicate_key_update(
            stock_name=stmt.inserted.stock_name,
            net_sell_qty=stmt.inserted.net_sell_qty,
            net_sell_amt=stmt.inserted.net_sell_amt,
            est_avg_price=stmt.inserted.est_avg_price,
            current_price=stmt.inserted.current_price,
            change_sign=stmt.inserted.change_sign,
            day_change=stmt.inserted.day_change,
            avg_price_change=stmt.inserted.avg_price_change,
            change_rate=stmt.inserted.change_rate,
            period_trade_volume=stmt.inserted.period_trade_volume,
            updated_at=func.now(),
        )

        await self.db.execute(stmt)

        return len(data)

    async def get_by_request(
        self,
        request: InvestorDailyTradeStockRequest
    ) -> List[InvestorDailyTradeStock]:
        conditions = [
            InvestorDailyTrade.start_date == request.strt_dt,
            InvestorDailyTrade.end_date == request.end_dt,
        ]
        if request.trde_tp is not None:
            conditions.append(InvestorDailyTrade.trade_type == request.trde_tp)
        if request.mrkt_tp is not None:
            conditions.append(InvestorDailyTrade.market_type == request.mrkt_tp)
        if request.invsr_tp is not None:
            conditions.append(InvestorDailyTrade.investor_type == request.invsr_tp)
        if request.stex_tp is not None:
            conditions.append(InvestorDailyTrade.exchange_type == request.stex_tp)

        stmt = select(InvestorDailyTrade).where(*conditions)

        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        return [
            InvestorDailyTradeStock(
                stk_cd=row.stock_code,
                stk_nm=row.stock_name,
                netslmt_qty=row.net_sell_qty or "",
                netslmt_amt=row.net_sell_amt or "",
                prsm_avg_pric=row.est_avg_price or "",
                cur_prc=row.current_price or "",
                pre_sig=row.change_sign or "",
                pred_pre=row.day_change or "",
                avg_pric_pre=row.avg_price_change or "",
                pre_rt=row.change_rate or "",
                dt_trde_qty=row.period_trade_volume or "",
            )
            for row in rows
        ]
