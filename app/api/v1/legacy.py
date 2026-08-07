from fastapi import APIRouter, status

from app.api.deps import TelegramUserDep
from app.api.v1.reviews import ReviewServiceDep
from app.api.v1.tasks import TaskServiceDep
from app.schemas.common import MessageResponse
from app.schemas.review import ReviewCreate, ReviewRead
from app.schemas.task import TaskCreate, TaskRead


router = APIRouter(tags=["Legacy"])


@router.post("/add", response_model=TaskRead, include_in_schema=False, status_code=status.HTTP_201_CREATED)
async def legacy_create_task(
    payload: TaskCreate,
    service: TaskServiceDep,
    telegram_user: TelegramUserDep,
) -> TaskRead:
    task = await service.create_task(payload, telegram_id=telegram_user.id)
    return TaskRead.model_validate(task)


@router.post(
    "/add_review",
    response_model=ReviewRead,
    include_in_schema=False,
    status_code=status.HTTP_201_CREATED,
)
async def legacy_create_review(
    payload: ReviewCreate,
    service: ReviewServiceDep,
    telegram_user: TelegramUserDep,
) -> ReviewRead:
    review = await service.create_review(payload, telegram_id=telegram_user.id)
    return ReviewRead.model_validate(review)


@router.delete(
    "/delete/{task_id}",
    response_model=MessageResponse,
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def legacy_delete_task(task_id: int, service: TaskServiceDep) -> MessageResponse:
    await service.delete_task(task_id)
    return MessageResponse(message=f"Заявка #{task_id} удалена")
