"""Market 도메인 API

실시간 시세 조회 API를 제공합니다.
"""
from app.api.market.market_controller import router as market_router

__all__ = ["market_router"]
