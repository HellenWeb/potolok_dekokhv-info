#!/usr/bin/env python3

"""

    date: 22.07.2026

    Конфиг файл со всеми переменными

"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=True)
    PROJECT_NAME: str = "API For POTOLKI DEKO"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    SECRET_KEY: str = "qwerty123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGIN: list = ["http://localhost:3000"]
    ALLOWED_HOSTS: list = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 60


setting = Settings()

