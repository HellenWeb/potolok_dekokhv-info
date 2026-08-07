from __future__ import annotations

from datetime import datetime

import phonenumbers
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import TaskStatus


class TaskCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    phone: str = Field(min_length=6, max_length=32)
    work_type: str = Field(min_length=2, max_length=128)
    address: str | None = Field(default=None, max_length=256)
    arrival_time: str = Field(min_length=2, max_length=128)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        try:
            phone = phonenumbers.parse(value, "RU")
        except phonenumbers.NumberParseException as exc:
            raise ValueError("Некорректный формат номера") from exc

        if not phonenumbers.is_valid_number(phone):
            raise ValueError("Некорректный номер телефона")
        return value


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskRead(BaseModel):
    id: int
    name: str
    phone: str
    work_type: str
    address: str | None = None
    arrival_time: str
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
