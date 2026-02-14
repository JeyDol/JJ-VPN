from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.vpn.db.base import Base


class IPPoolsOrm(Base):
    __tablename__ = "ip_pools"
    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(String(45), unique=True, index=True)
    is_allocated: Mapped[bool] = mapped_column(Boolean, default=False)
    peer_id: Mapped[int] = mapped_column(ForeignKey("peers.id", ondelete="SET NULL"), nullable=True)
    allocated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    peer = relationship("PeersOrm", back_populates="ip_pool")

