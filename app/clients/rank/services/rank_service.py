from typing import Optional, List

from app.clients.rank.dto.response.trade_rank_item import TradeRankResponse
from app.clients.rank.enums.mang_stk_incls import MangStkIncls
from app.clients.rank.enums.market_type import MarketType
from app.clients.rank.enums.stex_type import StexType
from app.clients.rank.repositories.rank_repository import RankRepository



class RankService:
    def __init__(self, rank_repository: RankRepository):
        self.rank_repository = rank_repository

    async def get_top_trading_volume_stocks(
        self,
        mrkt_tp: MarketType,
        mang_stk_incls: MangStkIncls,
        stex_tp: StexType,
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None
    ) -> TradeRankResponse:
        response = await self.rank_repository.get_rank_info(
            mrkt_tp=mrkt_tp,
            mang_stk_incls=mang_stk_incls,
            stex_tp=stex_tp
        )
        return response



