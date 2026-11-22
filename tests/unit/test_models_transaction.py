import pytest
from app.models.transaction import Transaction, TransactionStatus

def test_transaction_status_transitions():
    tx = Transaction(
        idempotency_key="key-test",
        source_account_id="acc-a",
        destination_account_id="acc-b",
        amount=50.0,
        status=TransactionStatus.INITIATED
    )
    assert tx.status == TransactionStatus.INITIATED
    tx.status = TransactionStatus.SETTLED
    assert tx.status == TransactionStatus.SETTLED
