import pytest
from app.models.ledger import LedgerEntry, EntryType

def test_ledger_entry_types():
    debit = LedgerEntry(
        transaction_id="tx-1",
        account_id="acc-1",
        entry_type=EntryType.DEBIT,
        amount=100.0,
        balance_after=400.0
    )
    credit = LedgerEntry(
        transaction_id="tx-1",
        account_id="acc-2",
        entry_type=EntryType.CREDIT,
        amount=100.0,
        balance_after=600.0
    )
    assert debit.entry_type == EntryType.DEBIT
    assert credit.entry_type == EntryType.CREDIT
    assert debit.amount == credit.amount
