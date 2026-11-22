import pytest
import uuid
from app.schemas.transaction import TransactionCreate
from app.models.transaction import TransactionStatus

def test_transaction_schema_validation():
    payload = TransactionCreate(
        idempotency_key=str(uuid.uuid4()),
        source_account_id=str(uuid.uuid4()),
        destination_account_id=str(uuid.uuid4()),
        amount=100.50,
        currency="USD"
    )
    assert payload.amount == 100.50
    assert payload.currency == "USD"
