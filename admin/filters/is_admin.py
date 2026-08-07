from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from admin.bot.config import settings


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.allowed_telegram_id = settings.ALLOWED_TELEGRAM_ID

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return bool(event.from_user and event.from_user.id == self.allowed_telegram_id)
