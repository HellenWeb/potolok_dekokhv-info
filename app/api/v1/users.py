from fastapi import APIRouter, status

from app.api.deps import TelegramUserDep
from app.schemas.user import TelegramUserRead


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=TelegramUserRead, status_code=status.HTTP_200_OK)
async def get_current_telegram_user(telegram_user: TelegramUserDep) -> TelegramUserRead:
    return TelegramUserRead.model_validate(telegram_user)
