#!/usr/bin/env python3

"""

    date: 22.07.2026

    -;- Файл для создание СУБД и их полей -;-

"""

from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Float
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from app.core.config import setting
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

## CONNECT

engine = create_async_engine(url=setting.DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

## Базовый модель для всех остальных моделей

class Base(AsyncAttrs, DeclarativeBase):
    pass

## Модель для записи пользователей

class Persons(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)

## Модель для записи замеров и прочих услуг в базу для удобной работы с ними

class Tasks(Base):
    
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(128), nullable=False)
    work_type: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(128))
    arrival_time = mapped_column(DateTime)
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

## Модель для записи отзывов и работы с ними

class Reviews(Base):

    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    title: Mapped[str] = mapped_column(String(128))
    stars: Mapped[int] = mapped_column(Float)
    date = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    

## Инициализируем базу данных

async def init_db():
    print("INIT DB")
    async with engine.begin() as conn:
        print("CREATE_ALL")
        await conn.run_sync(Base.metadata.create_all)

