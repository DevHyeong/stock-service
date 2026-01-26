from app.clients.rank.dto.response.trade_rank_item import TradeRankResponse
from app.clients.rank.enums.mang_stk_incls import MangStkIncls
from app.clients.rank.enums.market_type import MarketType
from app.clients.rank.enums.stex_type import StexType
from app.clients.rank.rank_client import RankClient
from app.common.auth_client import AuthClient


class RankRepository:
    def __init__(self, auth_client: AuthClient, rank_client: RankClient):
        self.auth_client = auth_client
        self.rank_client = rank_client


    async def get_rank_info(
        self,
        mrkt_tp: MarketType = MarketType.ALL,
        mang_stk_incls: MangStkIncls = MangStkIncls.EXCLUDE,
        stex_tp: StexType = StexType.KRX,
    ) -> TradeRankResponse:
        return await self.rank_client.get_trade_rank(
            access_token= await self.auth_client.ensure_token(),
            mrkt_tp= mrkt_tp,
            mang_stk_incls=mang_stk_incls,
            stex_tp=stex_tp
        )