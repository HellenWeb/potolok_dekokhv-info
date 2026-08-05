from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from admin.keyboards.inline import main_menu


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Админ-бот готов. Выберите раздел:", reply_markup=main_menu())

