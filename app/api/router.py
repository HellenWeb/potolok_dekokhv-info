from fastapi import APIRouter

from app.api.v1 import legacy, reviews, tasks, users
from app.core.config import get_settings


settings = get_settings()

api_router = APIRouter()
v1_router = APIRouter(prefix=settings.API_V1_STR)

v1_router.include_router(tasks.router)
v1_router.include_router(reviews.router)
v1_router.include_router(users.router)
v1_router.include_router(legacy.router)

api_router.include_router(v1_router)
