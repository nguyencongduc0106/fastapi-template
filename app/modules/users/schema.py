from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    password: str | None = Field(default=None, min_length=8)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
