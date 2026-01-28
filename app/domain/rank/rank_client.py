from typing import Optional

import httpx

from app.domain.rank.dto.response.trade_rank_item import TradeRankResponse, TradeRankItem
from app.domain.rank.enums.mang_stk_incls import MangStkIncls
from app.domain.rank.enums.market_type import MarketType
from app.domain.rank.enums.stex_type import StexType
from app.config import settings


class RankClient:

    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL

    # 거래대금 상위 요청
    async def get_trade_rank(
        self,
        access_token: str,
        mrkt_tp: MarketType = MarketType.ALL,  # 000:전체, 001:코스피, 101:코스닥
        mang_stk_incls: MangStkIncls = MangStkIncls.EXCLUDE,  # 0:관리종목 미포함, 1:포함
        stex_tp: StexType = StexType.KRX,  # 1:KRX, 2:NXT, 3:통합
        cont_yn: Optional[str] = None,
        next_key: Optional[str] = None,
    ) -> TradeRankResponse:
        """투자자별일별매매종목요청 (ka10058)"""

        headers = {
            "api-id": "ka10032",
            "authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        if cont_yn:
            headers["cont-yn"] = cont_yn
        if next_key:
            headers["next-key"] = next_key

        body = {
            "mrkt_tp": mrkt_tp.value,
            "mang_stk_incls": mang_stk_incls.value,
            "stex_tp": stex_tp.value,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/dostk/rkinfo",  # 실제 엔드포인트 확인 필요
                headers=headers,
                json=body,
            )
            response.raise_for_status()
            data = response.json()

        return TradeRankResponse(
            cont_yn=data.get("cont_yn"),
            next_key=data.get("next_key"),
            trde_prica_upper=[
                TradeRankItem(**item)
                for item in data.get("trde_prica_upper", [])
            ],
        )

