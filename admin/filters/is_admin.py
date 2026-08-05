from aiogram.filters import BaseFilter
from aiogram.types import Message

from admin.bot.config import settings


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = {
            int(admin_id)
            for admin_id in settings.ADMIN_IDS.split(",")
            if admin_id.strip().isdigit()
        }

    async def __call__(self, message: Message) -> bool:
        return bool(message.from_user and message.from_user.id in self.admin_ids)

