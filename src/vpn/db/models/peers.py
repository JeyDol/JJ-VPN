from decimal import Decimal
from email.policy import default

from sqlalchemy import ForeignKey, String, DateTime, Integer, func, Boolean, Numeric, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.vpn.db.base import Base


class PeersOrm(Base):
    __tablename__ = "peers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    device_name: Mapped[str] = mapped_column(String(100), default="Устройство")
    daily_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=10.00, server_default="10.00")
    last_charge_date: Mapped[Date] = mapped_column(Date, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("UsersOrm", back_populates="peers")

