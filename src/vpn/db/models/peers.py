

from sqlalchemy import ForeignKey, String, DateTime, Integer, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.vpn.db.base import Base


class PeersOrm(Base):
    __tablename__ = "peers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    public_key: Mapped[str] = mapped_column(String(64), unique=True)
    private_key_encrypted: Mapped[str]
    ip_address: Mapped[str] = mapped_column(String(45), unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="peers")

