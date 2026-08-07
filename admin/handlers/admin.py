import httpx

from aiogram import F, Router
from aiogram.types import CallbackQuery

from admin.filters.is_admin import IsAdmin
from admin.keyboards.inline import main_menu, task_actions
from admin.services.api_client import api_client


router = Router()
router.callback_query.filter(IsAdmin())


def format_task(task: dict) -> str:
    status_map = {
        "new": "Новая",
        "in_progress": "В работе",
        "done": "Выполнена",
        "cancelled": "Отменена",
    }

    return (
        "<b>Заявка #{id}</b>\n"
        "<b>Имя:</b> {name}\n"
        "<b>Телефон:</b> {phone}\n"
        "<b>Услуга:</b> {work_type}\n"
        "<b>Адрес:</b> {address}\n"
        "<b>Время приезда:</b> {arrival_time}\n"
        "<b>Статус:</b> {status}\n"
        "<b>Создана:</b> {created_at}"
    ).format(
        id=task.get("id", "-"),
        name=task.get("name") or "-",
        phone=task.get("phone") or "-",
        work_type=task.get("work_type") or "-",
        address=task.get("address") or "-",
        arrival_time=task.get("arrival_time") or "-",
        status=status_map.get(task.get("status"), task.get("status") or "-"),
        created_at=task.get("created_at") or "-",
    )


@router.callback_query(F.data == "show_tasks")
async def show_tasks(callback: CallbackQuery) -> None:
    await callback.answer("Обновляю список заявок...")

    try:
        tasks = await api_client.get_tasks()
    except httpx.HTTPError:
        await callback.message.answer("Не удалось получить заявки с API. Проверьте доступность сервера.")
        return

    if not tasks:
        await callback.message.answer(
            "<b>Активных заявок нет.</b>\n"
            "Когда появятся новые, они будут доступны здесь.",
            reply_markup=main_menu(),
        )
        return

    await callback.message.answer(
        f"<b>Найдено заявок:</b> {len(tasks)}\n"
        "Ниже каждая заявка выведена отдельной карточкой."
    )

    for task in tasks:
        await callback.message.answer(
            format_task(task),
            reply_markup=task_actions(int(task["id"])),
        )


@router.callback_query(F.data.startswith("close_task:"))
async def close_task(callback: CallbackQuery) -> None:
    task_id = int(callback.data.split(":", maxsplit=1)[1])

    try:
        await api_client.delete_task(task_id)
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            await callback.answer("Заявка уже удалена или не найдена.", show_alert=True)
            return
        await callback.answer("Ошибка при удалении заявки.", show_alert=True)
        return
    except httpx.HTTPError:
        await callback.answer("API сейчас недоступен.", show_alert=True)
        return

    if callback.message:
        await callback.message.edit_text(
            f"{callback.message.html_text}\n\n<i>Заявка закрыта.</i>",
            reply_markup=None,
        )

    await callback.answer("Заявка закрыта")
