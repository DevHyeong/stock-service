"""Sector 도메인 API

섹터/업종 관리 API를 제공합니다.
"""
from app.api.sector.sector_controller import router as sector_router

__all__ = ["sector_router"]
