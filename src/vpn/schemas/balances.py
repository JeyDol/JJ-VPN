from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, ConfigDict


class BalanceOperation(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма операции должна быть > 0")

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Сумма должна быть положительной")
        if v.as_tuple().exponent < -2:
            raise ValueError("Максимум  два знака после запятой")
        return v

    model_config = ConfigDict(from_attributes=True)