#!/usr/bin/env python3 

"""

    date: 22.07.2026

    Основой файл для работы с FastAPI и нашим Mini APP

"""

from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import setting
from app.middleware.security import add_security_headers, RateLimitMiddleware
from app.middleware.logging import LoggingMiddleware
from models import init_db
import requests as req
from datetime import datetime


class AddTask(BaseModel):
    tg_id: int
    name: str
    work_type: str
    address: str
    arrival_time: datetime
    created_at: datetime

class Review(BaseModel):
    tg_id: int
    name: str
    title: str
    date: datetime

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Initilization this application --;--")
    yield

app = FastAPI(
    title="DEKO POTOLKI KHV API",
    version="1.0.0"
)

## Логирование 

app.add_middleware(LoggingMiddleware)

app.add_middleware(add_security_headers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=setting.ALLOWED_HOSTS, 
)

app.add_middleware(RateLimitMiddleware)

@app.post(f"{setting.API_V1_STR}/add")
async def add_task(task: AddTask):
    user = await req.add_user(task.tg_id)
    await req.add_task(user.id, 
                       task.name, task.work_type, task.address,
                       task.arrival_time, task.created_at)
    return {"status": 200}

@app.get(f"{setting.API_V1_STR}/reviews")
async def show_reviews(tg_id: id):
    user = await req.add_user(task.tg_id)
    return await req.get_reviews(user.id)

@app.get(f"{setting.API_V1_STR}/tasks")
async def show_task(tg_id: id):
    user = await req.add_user(task.tg_id)
    return await req.get_tasks(user.id)

@app.post(f"{setting.API_V1_STR}/add_review")
async def add_review(review: Review):
    user = await req.add_user(task.tg_id)
    await req.add_reviews(user)

@app.get("/")
async def hello():
    return {"status": "Hello"}