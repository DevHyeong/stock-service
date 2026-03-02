"""Auth 도메인 API

인증 관련 API를 제공합니다.
"""
from app.api.auth.auth_controller import router as auth_router

__all__ = ["auth_router"]
