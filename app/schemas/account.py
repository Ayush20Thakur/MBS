from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class AccountCreate(BaseModel):
    currency: str = Field(default="USD", min_length=3, max_length=3)
    initial_deposit: float = Field(default=0.0, ge=0.0)


class AccountResponse(BaseModel):
    id: str
    user_id: str
    account_number: str
    currency: str
    balance: float
    is_frozen: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0.0)
