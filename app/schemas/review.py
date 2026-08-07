from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    title: str = Field(min_length=5, max_length=256)
    stars: int = Field(ge=1, le=5)


class ReviewRead(BaseModel):
    id: int
    name: str
    title: str
    stars: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
