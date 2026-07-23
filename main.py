#!/usr/bin/env python3 

"""

    date: 24.07.2026

    Основной файл для работы с FastAPI и нашим Mini APP

"""

from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import setting
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.logging import LoggingMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from models import init_db
import phonenumbers
from pydantic import BaseModel, field_validator, Field
import requests as req
from datetime import datetime

class AddTask(BaseModel):
    tg_id: int
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        try:
            phone = phonenumbers.parse(value, "RU")
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Неккоректный номер телефона")
        except phonenumbers.NumberParseException:
            raise ValueError("Некорректный формат номера")
        return value

    name: str = Field(max_length=128)
    work_type: str = Field(max_length=128)
    address: str = Field(max_length=128)
    arrival_time: datetime

class Review(BaseModel):
    tg_id: int
    name: str = Field(max_length=128)
    title: str = Field(max_length=256)
    stars: float = Field(max_length=10)

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Initilization this application --;--")
    yield

app = FastAPI(
    title="DEKO POTOLKI KHV API",
    version="1.0.0",
    lifespan=lifespan
) 

# Подключаем мидлы для безопасности и логирования :)

# ДЛЯ ПРОДА
# app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=setting.ALLOWED_HOSTS, 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(LoggingMiddleware)

# Роуты к нашему API

@app.post(f"{setting.API_V1_STR}/add")
async def add_task(task: AddTask):
    user = await req.add_user(task.tg_id)
    await req.add_task(user.id, 
                       task.name, task.phone, task.work_type, task.address,
                       task.arrival_time)

@app.get(f"{setting.API_V1_STR}/reviews")
async def show_reviews():
    return await req.get_reviews()

@app.get(f"{setting.API_V1_STR}/tasks")
async def show_task():
    return await req.get_tasks()

@app.post(f"{setting.API_V1_STR}/add_review")
async def add_review(review: Review):
    user = await req.add_user(review.tg_id)
    await req.add_reviews(user.id, review.name, review.title, review.stars)

@app.get("/")
async def hello():
    return {"status": "Time to CODE"}

# Запуск сервера --;--

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )