from decimal import Decimal
from enum import Enum

from sqlalchemy import ForeignKey, String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.vpn.db.base import Base


class TransactionType(str, Enum):
    DEPOSIT = "deposit"  # - пополнение
    CHARGE = "charge"    # - списание


class TransactionsOrm(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(20), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(String(255))
    peer_id: Mapped[int] = mapped_column(ForeignKey("peers.id", ondelete="SET NULL"), nullable=True)
    payment_provider: Mapped[str] = mapped_column(String(50), nullable=True)
    external_id: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UsersOrm", back_populates="transactions")
    peer = relationship("PeersOrm")

