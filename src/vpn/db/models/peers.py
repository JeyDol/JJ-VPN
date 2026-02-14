from decimal import Decimal

from sqlalchemy import ForeignKey, String, DateTime, Integer, func, Boolean, Numeric, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.vpn.db.base import Base


class PeersOrm(Base):
    __tablename__ = "peers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    public_key: Mapped[str] = mapped_column(String(64), unique=True)
    private_key_encrypted: Mapped[str] = mapped_column(Text)
    ip_pool_id: Mapped[int] = mapped_column(ForeignKey("ip_pools.id", ondelete="SET NULL"), nullable=True)
    daily_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=10.00, server_default="10.00")
    last_charge_date: Mapped[Date] = mapped_column(Date, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("UsersOrm", back_populates="peers")
    ip_pool = relationship("IPPoolsOrm", back_populates="peer")

