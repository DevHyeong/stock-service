from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Kiwoom Trading API"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Kiwoom API
    KIWOOM_APPKEY: str
    KIWOOM_SECRETKEY: str
    KIWOOM_BASE_URL: str

    # 데이터베이스 설정 추가
    DATABASE_URL: str
    DB_ECHO: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
