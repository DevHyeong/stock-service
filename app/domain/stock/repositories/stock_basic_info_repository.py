from sqlalchemy import func, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.stock.dto.stock_basic_info import StockBasicInfo
from app.models.stock_basic_info import StockBasicInfo as StockBasicInfoModel


class StockBasicInfoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, info: StockBasicInfo) -> None:
        data = {
            'stock_code': info.stk_cd,
            'stock_name': info.stk_nm,
            'setl_mm': info.setl_mm,
            'fav': info.fav,
            'fav_unit': info.fav_unit,
            'cap': info.cap,
            'flo_stk': info.flo_stk,
            'dstr_stk': info.dstr_stk,
            'dstr_rt': info.dstr_rt,
            'crd_rt': info.crd_rt,
            'mac': info.mac,
            'mac_wght': info.mac_wght,
            'for_exh_rt': info.for_exh_rt,
            'repl_pric': info.repl_pric,
            'cur_prc': info.cur_prc,
            'pre_sig': info.pre_sig,
            'pred_pre': info.pred_pre,
            'flu_rt': info.flu_rt,
            'trde_qty': info.trde_qty,
            'trde_pre': info.trde_pre,
            'open_pric': info.open_pric,
            'high_pric': info.high_pric,
            'low_pric': info.low_pric,
            'upl_pric': info.upl_pric,
            'lst_pric': info.lst_pric,
            'base_pric': info.base_pric,
            'exp_cntr_pric': info.exp_cntr_pric,
            'exp_cntr_qty': info.exp_cntr_qty,
            'oyr_hgst': info.oyr_hgst,
            'oyr_lwst': info.oyr_lwst,
            'hgst_250': info.hgst_250,
            'hgst_250_pric_dt': info.hgst_250_pric_dt,
            'hgst_250_pric_pre_rt': info.hgst_250_pric_pre_rt,
            'lwst_250': info.lwst_250,
            'lwst_250_pric_dt': info.lwst_250_pric_dt,
            'lwst_250_pric_pre_rt': info.lwst_250_pric_pre_rt,
            'per': info.per,
            'eps': info.eps,
            'roe': info.roe,
            'pbr': info.pbr,
            'ev': info.ev,
            'bps': info.bps,
            'sale_amt': info.sale_amt,
            'bus_pro': info.bus_pro,
            'cup_nga': info.cup_nga,
        }

        stmt = insert(StockBasicInfoModel).values(data)
        stmt = stmt.on_duplicate_key_update(
            **{k: stmt.inserted[k] for k in data if k != 'stock_code'},
            updated_at=func.now(),
        )

        await self.db.execute(stmt)

    async def get_by_code(self, stk_cd: str) -> StockBasicInfo | None:
        stmt = select(StockBasicInfoModel).where(StockBasicInfoModel.stock_code == stk_cd)
        result = await self.db.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
            return None

        return StockBasicInfo(
            stk_cd=row.stock_code,
            stk_nm=row.stock_name or "",
            setl_mm=row.setl_mm or "",
            fav=row.fav or "",
            fav_unit=row.fav_unit or "",
            cap=row.cap or "",
            flo_stk=row.flo_stk or "",
            dstr_stk=row.dstr_stk or "",
            dstr_rt=row.dstr_rt or "",
            crd_rt=row.crd_rt or "",
            mac=row.mac or "",
            mac_wght=row.mac_wght or "",
            for_exh_rt=row.for_exh_rt or "",
            repl_pric=row.repl_pric or "",
            cur_prc=row.cur_prc or "",
            pre_sig=row.pre_sig or "",
            pred_pre=row.pred_pre or "",
            flu_rt=row.flu_rt or "",
            trde_qty=row.trde_qty or "",
            trde_pre=row.trde_pre or "",
            open_pric=row.open_pric or "",
            high_pric=row.high_pric or "",
            low_pric=row.low_pric or "",
            upl_pric=row.upl_pric or "",
            lst_pric=row.lst_pric or "",
            base_pric=row.base_pric or "",
            exp_cntr_pric=row.exp_cntr_pric or "",
            exp_cntr_qty=row.exp_cntr_qty or "",
            oyr_hgst=row.oyr_hgst or "",
            oyr_lwst=row.oyr_lwst or "",
            **{"250hgst": row.hgst_250 or ""},
            **{"250hgst_pric_dt": row.hgst_250_pric_dt or ""},
            **{"250hgst_pric_pre_rt": row.hgst_250_pric_pre_rt or ""},
            **{"250lwst": row.lwst_250 or ""},
            **{"250lwst_pric_dt": row.lwst_250_pric_dt or ""},
            **{"250lwst_pric_pre_rt": row.lwst_250_pric_pre_rt or ""},
            per=row.per or "",
            eps=row.eps or "",
            roe=row.roe or "",
            pbr=row.pbr or "",
            ev=row.ev or "",
            bps=row.bps or "",
            sale_amt=row.sale_amt or "",
            bus_pro=row.bus_pro or "",
            cup_nga=row.cup_nga or "",
        )
