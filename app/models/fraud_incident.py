import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    CONFIRMED_FRAUD = "CONFIRMED_FRAUD"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class FraudIncident(Base):
    __tablename__ = "fraud_incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String(36), ForeignKey("transactions.id"), unique=True, nullable=False)
    risk_score = Column(Float, nullable=False)
    reasons = Column(Text, nullable=False)
    status = Column(SQLEnum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False)
    reviewed_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    transaction = relationship("Transaction", back_populates="incident")
