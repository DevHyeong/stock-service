"""Analysis 도메인 API

기술적 분석 API를 제공합니다.
"""
from app.api.analysis.analysis_controller import router as analysis_router

__all__ = ["analysis_router"]
