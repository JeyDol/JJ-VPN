from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict
from pydantic.v1 import EmailStr


class UserCreate(BaseModel):
    telegram_id: int = Field(..., ge=1)
    email: EmailStr | None = Field(default=None, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    telegram_id: int
    email: str | None = None
    balance: Decimal = Field(default=Decimal("0.00"), description="Баланс пользователя")
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserBalance(BaseModel):
    user_id: int
    telegram_id: int
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)

