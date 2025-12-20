from functools import lru_cache

from app.clients.kiwoom_api_client import kiwoom_api_client
from app.config import settings, Settings
from app.services.auth_service import auth_service
from app.services.kiwoom_service import kiwoom_service


@lru_cache
def get_settings() -> Settings:
    return settings

def get_kiwoom_service():
    '''키움 서비스 의존성'''
    return kiwoom_service


def get_auth_service():
    '''인증 서비스 의존성'''
    return auth_service

def get_kiwoom_api_client():
    '''키움 서비스 의존성'''
    return kiwoom_api_client