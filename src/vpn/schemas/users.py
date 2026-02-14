from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    telegram_id: int = Field(..., ge=1)
    email: str | None = Field(default=None, max_length=255)


class UserUpdate(BaseModel):
    email: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    subscription_expires_at: datetime | None = None


class UserRead(BaseModel):
    id: int
    telegram_id: int
    email: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    subscription_expires_at: datetime | None = None

