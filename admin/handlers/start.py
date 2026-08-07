from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from admin.filters.is_admin import IsAdmin
from admin.keyboards.inline import main_menu


router = Router()
router.message.filter(IsAdmin())


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "<b>Панель администратора</b>\n"
        "Нажмите кнопку ниже, чтобы получить актуальный список заявок.",
        reply_markup=main_menu(),
    )
