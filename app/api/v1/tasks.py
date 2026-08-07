from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import SessionDep, TelegramUserDep
from app.models.enums import TaskStatus
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.schemas.common import MessageResponse
from app.schemas.task import TaskCreate, TaskRead, TaskStatusUpdate
from app.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_service(session: SessionDep) -> TaskService:
    return TaskService(TaskRepository(session), UserRepository(session))


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    service: TaskServiceDep,
    telegram_user: TelegramUserDep,
) -> TaskRead:
    task = await service.create_task(payload, telegram_id=telegram_user.id)
    return TaskRead.model_validate(task)


@router.get("", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
async def list_tasks(
    service: TaskServiceDep,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
) -> list[TaskRead]:
    tasks = await service.list_tasks(limit=limit, offset=offset, status=status_filter)
    return [TaskRead.model_validate(task) for task in tasks]


@router.patch("/{task_id}/status", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    service: TaskServiceDep,
) -> TaskRead:
    task = await service.update_status(task_id, payload.status)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, service: TaskServiceDep) -> MessageResponse:
    await service.delete_task(task_id)
    return MessageResponse(message=f"Заявка #{task_id} удалена")
