import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    account_number = Column(String(32), unique=True, index=True, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    is_frozen = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    owner = relationship("User", back_populates="accounts")
    ledger_entries = relationship("LedgerEntry", back_populates="account")
