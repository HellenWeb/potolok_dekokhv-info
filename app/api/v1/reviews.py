from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import SessionDep, TelegramUserDep
from app.repositories.review import ReviewRepository
from app.repositories.user import UserRepository
from app.schemas.review import ReviewCreate, ReviewRead
from app.services.review_service import ReviewService


router = APIRouter(prefix="/reviews", tags=["Reviews"])


def get_review_service(session: SessionDep) -> ReviewService:
    return ReviewService(ReviewRepository(session), UserRepository(session))


ReviewServiceDep = Annotated[ReviewService, Depends(get_review_service)]


@router.get("", response_model=list[ReviewRead], status_code=status.HTTP_200_OK)
async def list_reviews(
    service: ReviewServiceDep,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[ReviewRead]:
    reviews = await service.list_reviews(limit=limit, offset=offset)
    return [ReviewRead.model_validate(review) for review in reviews]


@router.post("", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreate,
    service: ReviewServiceDep,
    telegram_user: TelegramUserDep,
) -> ReviewRead:
    review = await service.create_review(payload, telegram_id=telegram_user.id)
    return ReviewRead.model_validate(review)
