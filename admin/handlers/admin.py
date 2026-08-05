from aiogram import F, Router
from aiogram.types import CallbackQuery

from admin.services.api_client import api_client


router = Router()


@router.callback_query(F.data == "show_tasks")
async def show_tasks(callback: CallbackQuery) -> None:
    tasks = await api_client.get_tasks()
    if not tasks:
        await callback.message.answer("Заявок пока нет.")
        await callback.answer()
        return

    text = "\n\n".join(
        f"#{item['id']} {item.get('name', '')}\n"
        f"Телефон: {item.get('phone', '-')}\n"
        f"Адрес: {item.get('address', '-')}"
        for item in tasks[:10]
    )
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "show_reviews")
async def show_reviews(callback: CallbackQuery) -> None:
    reviews = await api_client.get_reviews()
    if not reviews:
        await callback.message.answer("Отзывов пока нет.")
        await callback.answer()
        return

    text = "\n\n".join(
        f"#{item['id']} {item.get('name', '')}\n"
        f"Оценка: {item.get('stars', '-')}\n"
        f"{item.get('title', '')}"
        for item in reviews[:10]
    )
    await callback.message.answer(text)
    await callback.answer()

