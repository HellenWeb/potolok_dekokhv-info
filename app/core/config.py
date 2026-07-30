#!/usr/bin/env python3

"""

    date: 22.07.2026

    Конфиг файл со всеми переменными

"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=True)
    PROJECT_NAME: str = "API For POTOLKI DEKO"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
    ALLOWED_HOSTS: list = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 60


setting = Settings()

