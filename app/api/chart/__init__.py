"""Chart 도메인 API

차트 데이터 조회 및 동기화 API를 제공합니다.
"""
from app.api.chart.chart_controller import router as chart_router

__all__ = ["chart_router"]
