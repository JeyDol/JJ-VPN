from sqlalchemy import ForeignKey, String, DateTime, func, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.vpn.db.base import Base


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    peer_id: Mapped[int] = mapped_column(ForeignKey("peers.id", ondelete="SET NULL"), nullable=True)
    plan: Mapped[str] = mapped_column(String(50))
    price: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expired_at: Mapped[DateTime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", backref="subscriptions")
    peer = relationship("Peer", backref="subscriptions")


