"""Rank 도메인 API

거래대금 순위 조회 API를 제공합니다.
"""
from app.api.rank.rank_controller import router as rank_router

__all__ = ["rank_router"]
