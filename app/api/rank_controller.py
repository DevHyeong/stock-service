# app/api/rank_controller.py
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.domain.rank.dto import TradeRankResponse
from app.domain.rank.enums import MangStkIncls
from app.domain.rank.enums import MarketType
from app.domain.rank.enums import StexType
from app.domain.rank.services.rank_service import RankService
from app.containers import Container

router = APIRouter(prefix="/rank", tags=["rank"])


@router.get("/trade-price", response_model=TradeRankResponse)
@inject
async def get_trade_price_rank(
    mrkt_tp: MarketType = Query(..., description="시장 유형"),
    mang_stk_incls: MangStkIncls = Query(..., description="관리종목 포함 여부"),
    stex_tp: StexType = Query(..., description="거래소 유형"),
    cont_yn: Optional[str] = Query(None, description="연속 조회 여부"),
    next_key: Optional[str] = Query(None, description="다음 키"),
    rank_service: RankService = Depends(Provide[Container.rank_service])
) -> TradeRankResponse:
    return await rank_service.get_top_trading_volume_stocks(
        mrkt_tp=mrkt_tp,
        mang_stk_incls=mang_stk_incls,
        stex_tp=stex_tp,
        cont_yn=cont_yn,
        next_key=next_key
    )
