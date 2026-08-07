from __future__ import annotations

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from pydantic import BaseModel, ValidationError

from app.core.exceptions import UnauthorizedError


class TelegramUser(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class TelegramInitData(BaseModel):
    auth_date: int
    query_id: str | None = None
    user: TelegramUser
    raw: dict[str, str]


def validate_telegram_init_data(
    init_data: str,
    *,
    bot_token: str,
    max_age_seconds: int,
) -> TelegramInitData:
    if not init_data:
        raise UnauthorizedError(
            "Telegram init data is required",
            error_code="telegram_init_data_missing",
        )

    payload = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = payload.pop("hash", None)
    if not received_hash:
        raise UnauthorizedError(
            "Telegram init data signature is missing",
            error_code="telegram_signature_missing",
        )

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(payload.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    expected_hash = hmac.new(
        secret_key,
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_hash, received_hash):
        raise UnauthorizedError(
            "Telegram init data validation failed",
            error_code="telegram_signature_invalid",
        )

    auth_date_raw = payload.get("auth_date")
    if not auth_date_raw or not auth_date_raw.isdigit():
        raise UnauthorizedError(
            "Telegram auth date is invalid",
            error_code="telegram_auth_date_invalid",
        )

    auth_date = int(auth_date_raw)
    if max_age_seconds > 0 and auth_date < int(time.time()) - max_age_seconds:
        raise UnauthorizedError(
            "Telegram session has expired",
            error_code="telegram_session_expired",
        )

    user_raw = payload.get("user")
    if not user_raw:
        raise UnauthorizedError(
            "Telegram user payload is missing",
            error_code="telegram_user_missing",
        )

    try:
        user = TelegramUser.model_validate(json.loads(user_raw))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise UnauthorizedError(
            "Telegram user payload is invalid",
            error_code="telegram_user_invalid",
        ) from exc

    return TelegramInitData(auth_date=auth_date, query_id=payload.get("query_id"), user=user, raw=payload)
