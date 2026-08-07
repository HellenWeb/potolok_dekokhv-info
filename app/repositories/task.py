from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import TaskStatus
from app.models.task import Task


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        user_id: int,
        name: str,
        phone: str,
        work_type: str,
        address: str | None,
        arrival_time: str,
    ) -> Task:
        task = Task(
            user_id=user_id,
            name=name,
            phone=phone,
            work_type=work_type,
            address=address,
            arrival_time=arrival_time,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: TaskStatus | None = None,
    ) -> list[Task]:
        query = select(Task).order_by(desc(Task.created_at)).offset(offset).limit(limit)
        if status is not None:
            query = query.where(Task.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Task | None:
        return await self.session.get(Task, task_id)

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.commit()

    async def update_status(self, task: Task, status: TaskStatus) -> Task:
        task.status = status
        await self.session.commit()
        await self.session.refresh(task)
        return task
