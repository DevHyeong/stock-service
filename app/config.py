from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Kiwoom Trading API"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Kiwoom API
    KIWOOM_APPKEY: str = "" # "b9SoeFzHpcbrTYSxdLld3XPkHH7OlHQ_bSlE4eEweEo"
    KIWOOM_SECRETKEY: str = "" #"9Rj-zKHHFnvEFYO07NABIp-tDdvmn3afWGPdtPSkWqU"
    KIWOOM_BASE_URL: str = "" #"https://api.kiwoom.com"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
