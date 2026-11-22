import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class TransactionStatus(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    APPROVED = "APPROVED"
    FLAGGED = "FLAGGED"
    REJECTED = "REJECTED"
    SETTLED = "SETTLED"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idempotency_key = Column(String(128), unique=True, index=True, nullable=False)
    source_account_id = Column(String(36), ForeignKey("accounts.id"), nullable=False, index=True)
    destination_account_id = Column(String(36), ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.INITIATED, nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    client_ip = Column(String(45), nullable=True)
    country_code = Column(String(2), default="US", nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    source_account = relationship("Account", foreign_keys=[source_account_id])
    destination_account = relationship("Account", foreign_keys=[destination_account_id])
    ledger_entries = relationship("LedgerEntry", back_populates="transaction", cascade="all, delete-orphan")
    incident = relationship("FraudIncident", back_populates="transaction", uselist=False)
