from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionStatus


class TransactionCreate(BaseModel):
    idempotency_key: str = Field(..., min_length=8, max_length=128)
    source_account_id: str
    destination_account_id: str
    amount: float = Field(..., gt=0.0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    client_ip: Optional[str] = None
    country_code: Optional[str] = "US"


class TransactionResponse(BaseModel):
    id: str
    idempotency_key: str
    source_account_id: str
    destination_account_id: str
    amount: float
    currency: str
    status: TransactionStatus
    risk_score: float
    client_ip: Optional[str] = None
    country_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
