#!/usr/bin/env python3

"""

    Запросы для базы в виде функций -;-

"""

from sqlalchemy import select, update, delete, func
from models import async_session, Persons, Tasks, Reviews
from fastapi import HTTPException, status
from app.core.config import setting
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class TaskSchema(BaseModel):
    id: int
    name: str
    phone: str
    work_type: str
    address: str
    arrival_time: str
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

async def delete_task(task_id):
    async with async_session() as session:
        task = await session.execute(select(Tasks).where(Tasks.id == task_id))
        task_i = task.scalars().first()
        if not task_i:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заявка с id={task_id} не найдена"
            )
        await session.delete(task_i)
        await session.commit()

async def add_task(user_id, name, phone, work_type, address, arrival_time):
    async with async_session() as session:
        new_task = Tasks(
            name=name,
            phone=phone,
            work_type=work_type,
            address=address,
            arrival_time=arrival_time,
            user=user_id
        )
        session.add(new_task)
        await session.commit()

async def add_reviews(user_id, name, title, stars):
    async with async_session() as session:
        review = await session.scalar(select(Reviews).where(Reviews.user == user_id))
        if review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Отзыв от вас уже был оставлен ранее"
            )
        
        new_review = Reviews(
            name=name,
            title=title,
            stars=stars,
            user=user_id
        )
        session.add(new_review)
        await session.commit()

async def get_reviews():
    async with async_session() as session:
        result = await session.execute(select(Reviews))
        review = result.scalars().all()

        return [
            {
                "id": r.id,
                "name": r.name,
                "title": r.title,
                "stars": r.stars,
                "date": r.date,
            } for r in review
        ]
    
async def get_tasks():
    async with async_session() as session:
        result = await session.execute(select(Tasks))
        task = result.scalars().all()

        return [
            {
                "id": r.id,
                "name": r.name,
                "phone": r.phone,
                "work_type": r.work_type,
                "address": r.address,
                "arrival_time": r.arrival_time,
                "created_at": r.created_at
            } for r in task
        ]






