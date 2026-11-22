from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.ledger import EntryType


class LedgerEntryResponse(BaseModel):
    id: str
    transaction_id: str
    account_id: str
    entry_type: EntryType
    amount: float
    balance_after: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LedgerBalanceAudit(BaseModel):
    account_id: str
    account_balance: float
    sum_credits: float
    sum_debits: float
    calculated_balance: float
    is_balanced: bool
