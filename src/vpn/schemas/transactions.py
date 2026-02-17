from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from src.vpn.db.models.transactions import TransactionType


class TransactionCreate(BaseModel):
    user_id: int
    type: TransactionType
    amount: Decimal = Field(..., gt = 0)
    description: str = Field(..., max_length=255)
    peer_id: int | None = None
    payment_provider: str | None = Field(default=None, max_length=255)
    external_id: str | None = Field(default=None, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class TransactionRead(BaseModel):
    id: int
    user_id: int
    type: str
    amount: Decimal
    description: str
    peer_id: int | None = None
    payment_provider : str | None = None
    external_id: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

