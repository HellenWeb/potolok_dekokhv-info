from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review


class ReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, *, limit: int = 50, offset: int = 0) -> list[Review]:
        query = select(Review).order_by(desc(Review.created_at)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_user_id(self, user_id: int) -> Review | None:
        result = await self.session.execute(select(Review).where(Review.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, *, user_id: int, name: str, title: str, stars: int) -> Review:
        review = Review(user_id=user_id, name=name, title=title, stars=stars)
        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(review)
        return review
