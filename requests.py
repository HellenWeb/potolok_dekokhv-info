#!/usr/bin/env python3

"""

    Запросы для базы в виде функций -;-

"""

from sqlalchemy import select, update, delete, func
from models import async_session, Persons, Tasks, Reviews
from app.core.config import setting
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class TaskSchema(BaseModel):
    id: int
    work_type: str
    address: str
    arrival_time: datetime
    created_at: datetime
    user: str

    model_config = ConfigDict(from_attributes=True)

class ReviewsSchema(BaseModel):
    id: int
    name: str
    title: str
    stars: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)

async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Persons).where(Persons.tg_id == tg_id))
        if user:
            return user
        new_user = Persons(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def add_task(user_id):
    async with async_session() as session:
        new_task = Tasks(
            work_type=work_type,
            address=address,
            arrival_time=arrival_time,
            user=user_id
        )
        session.add(new_task)
        await session.commit()

async def add_reviews(user_id):
    async with async_session() as session:
        new_review = Reviews(
            name=name,
            title=title,
            stars=stars,
            user=user_id
        )
        session.add(new_review)
        await session.commit()

async def get_reviews(user_id):
    async with async_session() as session:
        review = await session.scalar(select(Reviews).where(Reviews.id == user_id))

        serialized_reviews = [
            ReviewsSchema.model_validation(t).model_dump() for t in review
        ]

        return serialized_reviews
    
async def get_tasks(user_id):
    async with async_session() as session:
        task = await session.scalar(select(Tasks).where(Tasks.id == user_id))

        serialized_tasks = [
            TaskSchema.model_validation(t).model_dump() for t in task
        ]

        return serialized_tasks






