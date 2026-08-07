from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


def _read_admin_bot_token() -> str | None:
    admin_env_path = BASE_DIR / "admin" / ".env"
    if not admin_env_path.exists():
        return None

    for raw_line in admin_env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", maxsplit=1)
        if key.strip() == "BOT_TOKEN":
            return value.strip()

    return None


class DatabaseSettings(BaseModel):
    url: str


class SecuritySettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cors_origins: list[str]
    cors_origin_regex: str | None = None
    allowed_hosts: list[str]
    rate_limit_per_minute: int


class TelegramSettings(BaseModel):
    bot_token: str | None = None
    admin_ids: list[int] = Field(default_factory=list)
    init_data_header: str
    init_data_max_age: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(BASE_DIR / ".env"), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    PROJECT_NAME: str = "DEKO POTOLKI KHV API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )
    BACKEND_CORS_ORIGIN_REGEX: str | None = None
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: ["*"])
    RATE_LIMIT_PER_MINUTE: int = 60

    TELEGRAM_BOT_TOKEN: str | None = None
    BOT_TOKEN: str | None = None
    ADMIN_IDS: list[int] = Field(default_factory=list)
    TELEGRAM_INIT_DATA_HEADER: str = "X-Telegram-Init-Data"
    TELEGRAM_INIT_DATA_MAX_AGE: int = 60 * 60 * 24

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "prod"

    @property
    def database(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.DATABASE_URL)

    @property
    def security(self) -> SecuritySettings:
        cors_origin_regex = self.BACKEND_CORS_ORIGIN_REGEX
        if cors_origin_regex is None and self.ENVIRONMENT == "dev":
            cors_origin_regex = r"^https://.*\.ngrok-free\.app$"

        return SecuritySettings(
            secret_key=self.SECRET_KEY,
            algorithm=self.ALGORITHM,
            access_token_expire_minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES,
            cors_origins=self.BACKEND_CORS_ORIGINS,
            cors_origin_regex=cors_origin_regex,
            allowed_hosts=self.ALLOWED_HOSTS,
            rate_limit_per_minute=self.RATE_LIMIT_PER_MINUTE,
        )

    @property
    def telegram(self) -> TelegramSettings:
        return TelegramSettings(
            bot_token=self.TELEGRAM_BOT_TOKEN or self.BOT_TOKEN or _read_admin_bot_token(),
            admin_ids=self.ADMIN_IDS,
            init_data_header=self.TELEGRAM_INIT_DATA_HEADER,
            init_data_max_age=self.TELEGRAM_INIT_DATA_MAX_AGE,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


setting = get_settings()
