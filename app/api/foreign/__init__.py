"""Foreign 도메인 API

외국인 매매동향 조회 API를 제공합니다.
"""
from app.api.foreign.foreign_controller import router as foreign_router

__all__ = ["foreign_router"]
