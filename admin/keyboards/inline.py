from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Заявки", callback_data="show_tasks")],
            [InlineKeyboardButton(text="Отзывы", callback_data="show_reviews")],
        ]
    )

