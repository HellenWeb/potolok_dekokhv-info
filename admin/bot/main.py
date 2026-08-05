import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from admin.bot.config import settings
from admin.bot.database import init_db
from admin.handlers.admin import router as admin_router
from admin.handlers.start import router as start_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await init_db()

    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

