from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.fraud_rule import RuleType, RuleAction
from app.models.fraud_incident import IncidentStatus


class FraudRuleCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    rule_type: RuleType
    threshold: Optional[float] = None
    restriction_value: Optional[str] = None
    action: RuleAction = RuleAction.REJECT
    is_active: bool = True


class FraudRuleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    rule_type: RuleType
    threshold: Optional[float]
    restriction_value: Optional[str]
    action: RuleAction
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class IncidentResponse(BaseModel):
    id: str
    transaction_id: str
    risk_score: float
    reasons: str
    status: IncidentStatus
    reviewed_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus
