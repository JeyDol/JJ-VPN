
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class PeerCreate(BaseModel):
    user_id: int = Field(..., ge=1, description="ID пользователя")
    daily_cost: Decimal = Field(default=Decimal("10.00"), gt=0, description="Стоимость за день")


    model_config = ConfigDict(from_attributes=True)


class PeerUpdate(BaseModel):
    daily_cost: Decimal | None = Field(default=None, gt=0, description="Новая стоимость за день")

    model_config = ConfigDict(from_attributes=True)


class PeerRead(BaseModel):
    id: int
    user_id: int
    public_key: str
    ip_pool_id: int | None = None
    daily_cost: Decimal
    last_charge_date: date | None = None
    created_at: datetime
    revoked_at: datetime | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class PeerWithIp(BaseModel):
    id: int
    user_id: int
    public_key: str
    ip_address: str | None = Field(default=None, description="IP адрес из ip_pool")
    daily_cost: Decimal
    last_charge_date: date | None = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PeerConfig(BaseModel):
    peer_id: int
    public_key: str
    private_key: str
    ip_address: str
    server_public_key: str
    server_endpoint: str
    allowed_ips: str = Field(default="0.0.0.0/0", description="Разрешённые IP")
    dns: str = Field(default="1.1.1.1, 1.0.0.1", description="DNS серверы")

    model_config = ConfigDict(from_attributes=True)

    def to_wireguard_config(self) -> str:
        return f"""[Interface]
    PrivateKey = {self.private_key}
    Address = {self.ip_address}/32
    DNS = {self.dns}

    [Peer]
    PublicKey = {self.server_public_key}
    Endpoint = {self.server_endpoint}
    AllowedIPs = {self.allowed_ips}
    PersistentKeepalive = 25
    """


class PeerStats(BaseModel):
    peer_id: int
    user_id: int
    total_days_active: int
    total_cost: Decimal
    last_charge_date: Decimal | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

