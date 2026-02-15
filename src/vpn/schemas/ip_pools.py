from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class IPPoolCreate(BaseModel):
    ip_address: str = Field(..., description="IP адрес")

    model_config = ConfigDict(from_attributes=True)


class IPPoolUpdate(BaseModel):
    is_allocated: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class IPPoolRead(BaseModel):
    id: int
    ip_address: str
    is_allocated: bool
    peer_id: int | None = None
    allocated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class IPPoolStats(BaseModel):
    total_ips: int
    allocated_ips: int
    free_ips: int
    utilization_percent: float

    model_config = ConfigDict(from_attributes=True)