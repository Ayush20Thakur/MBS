import pytest
import uuid
from app.models.account import Account
from app.models.transaction import Transaction, TransactionStatus
from app.models.ledger import EntryType
from app.services.ledger_service import LedgerService
from app.core.exceptions import InsufficientFundsError


@pytest.mark.asyncio
async def test_ledger_transfer_preserves_zero_sum_invariant(db_session):
    # Setup test accounts
    acc_a = Account(user_id=str(uuid.uuid4()), account_number="TEST001", balance=500.0)
    acc_b = Account(user_id=str(uuid.uuid4()), account_number="TEST002", balance=100.0)
    db_session.add_all([acc_a, acc_b])
    await db_session.flush()

    tx = Transaction(
        idempotency_key=str(uuid.uuid4()),
        source_account_id=acc_a.id,
        destination_account_id=acc_b.id,
        amount=150.0,
        status=TransactionStatus.PROCESSING
    )
    db_session.add(tx)
    await db_session.flush()

    # Execute transfer
    debit, credit = await LedgerService.record_transfer(
        db=db_session,
        transaction=tx,
        source=acc_a,
        destination=acc_b,
        amount=150.0
    )

    # Invariants
    assert debit.amount == credit.amount == 150.0
    assert debit.entry_type == EntryType.DEBIT
    assert credit.entry_type == EntryType.CREDIT
    assert acc_a.balance == 350.0
    assert acc_b.balance == 250.0


@pytest.mark.asyncio
async def test_ledger_transfer_rejects_insufficient_funds(db_session):
    acc_a = Account(user_id=str(uuid.uuid4()), account_number="TEST003", balance=50.0)
    acc_b = Account(user_id=str(uuid.uuid4()), account_number="TEST004", balance=100.0)
    db_session.add_all([acc_a, acc_b])
    await db_session.flush()

    tx = Transaction(
        idempotency_key=str(uuid.uuid4()),
        source_account_id=acc_a.id,
        destination_account_id=acc_b.id,
        amount=500.0,
        status=TransactionStatus.PROCESSING
    )
    db_session.add(tx)
    await db_session.flush()

    with pytest.raises(InsufficientFundsError):
        await LedgerService.record_transfer(
            db=db_session,
            transaction=tx,
            source=acc_a,
            destination=acc_b,
            amount=500.0
        )
