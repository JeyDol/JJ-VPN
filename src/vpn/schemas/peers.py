
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class PeerCreate(BaseModel):
    user_id: int = Field(..., ge=1, description="ID пользователя")
    uuid: str = Field(..., min_length=36, max_length=36)
    device_name: str = Field(default="Устройство", max_length=100)
    daily_cost: Decimal = Field(default=Decimal("10.00"), gt=0, description="Стоимость за день")


    model_config = ConfigDict(from_attributes=True)


class PeerUpdate(BaseModel):
    device_name: str | None = Field(default=None, max_length=100)
    daily_cost: Decimal | None = Field(default=None, gt=0, description="Новая стоимость за день")

    model_config = ConfigDict(from_attributes=True)


class PeerRead(BaseModel):
    id: int
    user_id: int
    uuid: str
    device_name: str
    daily_cost: Decimal
    last_charge_date: date | None = None
    created_at: datetime
    revoked_at: datetime | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class VLESSConfig(BaseModel):
    peer_id: int
    uuid: str
    device_name: str
    server_address: str
    server_port: int
    public_key: str
    short_id: str
    sni: str

    def to_vless_link(self) -> str:
        return (
            f"vless://{self.uuid}@{self.server_address}:{self.server_port}"
            f"?security=reality"
            f"&sni={self.sni}"
            f"&fp=chrome"
            f"&pbk={self.public_key}"
            f"&sid={self.short_id}"
            f"&type=tcp"
            f"&flow=xtls-rprx-vision"
            f"#{self.device_name}"
        )

    model_config = {"from_attributes": True}


class PeerStats(BaseModel):
    peer_id: int
    user_id: int
    total_days_active: int
    total_cost: Decimal
    last_charge_date: date | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

