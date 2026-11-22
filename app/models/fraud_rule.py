import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, Enum as SQLEnum
from app.core.database import Base


class RuleType(str, Enum):
    VELOCITY_COUNT = "VELOCITY_COUNT"
    AMOUNT_CEILING = "AMOUNT_CEILING"
    COUNTRY_RESTRICTION = "COUNTRY_RESTRICTION"


class RuleAction(str, Enum):
    FLAG = "FLAG"
    REJECT = "REJECT"


class FraudRule(Base):
    __tablename__ = "fraud_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    rule_type = Column(SQLEnum(RuleType), nullable=False)
    threshold = Column(Float, nullable=True)
    restriction_value = Column(String(100), nullable=True)
    action = Column(SQLEnum(RuleAction), default=RuleAction.REJECT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
