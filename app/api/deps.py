from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import TelegramUser, validate_telegram_init_data
from app.db.session import get_session


def get_app_settings() -> Settings:
    return get_settings()


SettingsDep = Annotated[Settings, Depends(get_app_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def require_telegram_user(
    settings: SettingsDep,
    request: Request,
) -> TelegramUser:
    telegram_init_data = request.headers.get(settings.telegram.init_data_header)

    if not telegram_init_data and not settings.is_production:
        debug_user_id = request.headers.get("X-Debug-Telegram-Id", "0")
        if not debug_user_id.isdigit():
            debug_user_id = "0"
        return TelegramUser(id=int(debug_user_id), first_name="Dev", username="dev")

    if not telegram_init_data:
        raise UnauthorizedError(
            "Требуется валидный Telegram initData",
            error_code="telegram_init_data_missing",
        )

    if not settings.telegram.bot_token and not settings.is_production:
        return TelegramUser(id=0, first_name="Dev", username="dev")

    if not settings.telegram.bot_token:
        raise UnauthorizedError(
            "Telegram bot token is not configured on the backend",
            error_code="telegram_bot_token_missing",
        )

    payload = validate_telegram_init_data(
        telegram_init_data,
        bot_token=settings.telegram.bot_token,
        max_age_seconds=settings.telegram.init_data_max_age,
    )
    return payload.user


TelegramUserDep = Annotated[TelegramUser, Depends(require_telegram_user)]
