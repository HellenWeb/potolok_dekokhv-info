from __future__ import annotations

from app.core.exceptions import NotFoundError
from app.models.enums import TaskStatus
from app.models.task import Task
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.schemas.task import TaskCreate


class TaskService:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository) -> None:
        self.task_repository = task_repository
        self.user_repository = user_repository

    async def create_task(self, payload: TaskCreate, *, telegram_id: int) -> Task:
        user = await self.user_repository.get_or_create_by_telegram_id(telegram_id)
        return await self.task_repository.create(
            user_id=user.id,
            name=payload.name,
            phone=payload.phone,
            work_type=payload.work_type,
            address=payload.address,
            arrival_time=payload.arrival_time,
        )

    async def list_tasks(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        return await self.task_repository.list(limit=limit, offset=offset, status=status)

    async def delete_task(self, task_id: int) -> None:
        task = await self.task_repository.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Заявка с id={task_id} не найдена", error_code="task_not_found")
        await self.task_repository.delete(task)

    async def update_status(self, task_id: int, status: TaskStatus) -> Task:
        task = await self.task_repository.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Заявка с id={task_id} не найдена", error_code="task_not_found")
        return await self.task_repository.update_status(task, status)
