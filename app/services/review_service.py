from __future__ import annotations

from app.core.exceptions import ConflictError
from app.models.review import Review
from app.repositories.review import ReviewRepository
from app.repositories.user import UserRepository
from app.schemas.review import ReviewCreate


class ReviewService:
    def __init__(self, review_repository: ReviewRepository, user_repository: UserRepository) -> None:
        self.review_repository = review_repository
        self.user_repository = user_repository

    async def list_reviews(self, *, limit: int = 50, offset: int = 0) -> list[Review]:
        return await self.review_repository.list(limit=limit, offset=offset)

    async def create_review(self, payload: ReviewCreate, *, telegram_id: int) -> Review:
        user = await self.user_repository.get_or_create_by_telegram_id(telegram_id)
        existing_review = await self.review_repository.get_by_user_id(user.id)
        if existing_review is not None:
            raise ConflictError(
                "Отзыв от вас уже был оставлен ранее",
                error_code="review_already_exists",
            )
        return await self.review_repository.create(
            user_id=user.id,
            name=payload.name,
            title=payload.title,
            stars=payload.stars,
        )
