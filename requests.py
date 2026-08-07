from __future__ import annotations

from app.core.exceptions import ConflictError, NotFoundError
from app.db.session import AsyncSessionLocal
from app.repositories.review import ReviewRepository
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.schemas.review import ReviewRead
from app.schemas.task import TaskRead


async def add_user(tg_id: int):
    async with AsyncSessionLocal() as session:
        return await UserRepository(session).get_or_create_by_telegram_id(tg_id)


async def delete_task(task_id: int) -> None:
    async with AsyncSessionLocal() as session:
        task_repository = TaskRepository(session)
        task = await task_repository.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Заявка с id={task_id} не найдена", error_code="task_not_found")
        await task_repository.delete(task)


async def add_task(
    user_id: int,
    name: str,
    phone: str,
    work_type: str,
    address: str | None,
    arrival_time: str,
) -> None:
    async with AsyncSessionLocal() as session:
        await TaskRepository(session).create(
            user_id=user_id,
            name=name,
            phone=phone,
            work_type=work_type,
            address=address,
            arrival_time=arrival_time,
        )


async def add_reviews(user_id: int, name: str, title: str, stars: int, date: str | None = None) -> None:
    async with AsyncSessionLocal() as session:
        review_repository = ReviewRepository(session)
        existing_review = await review_repository.get_by_user_id(user_id)
        if existing_review is not None:
            raise ConflictError(
                "Отзыв от вас уже был оставлен ранее",
                error_code="review_already_exists",
            )
        await review_repository.create(user_id=user_id, name=name, title=title, stars=stars)


async def get_reviews() -> list[dict]:
    async with AsyncSessionLocal() as session:
        reviews = await ReviewRepository(session).list(limit=100, offset=0)
        return [ReviewRead.model_validate(review).model_dump(mode="json") for review in reviews]


async def get_tasks() -> list[dict]:
    async with AsyncSessionLocal() as session:
        tasks = await TaskRepository(session).list(limit=100, offset=0)
        return [TaskRead.model_validate(task).model_dump(mode="json") for task in tasks]





