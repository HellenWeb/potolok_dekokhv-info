from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(BASE_DIR / ".env"), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    BOT_TOKEN: str
    API_BASE_URL: str = "http://127.0.0.1:8000"
    API_V1_STR: str = "/api/v1"
    ALLOWED_TELEGRAM_ID: int = Field(..., description="Telegram ID владельца бота")


settings = Settings()
