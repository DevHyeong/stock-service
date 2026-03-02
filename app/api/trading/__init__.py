"""Trading 도메인 API

거래 정보 조회 및 동기화 API를 제공합니다.
"""
from app.api.trading.trading_controller import router as trading_router

__all__ = ["trading_router"]
