import pytest
from app.models.account import Account

def test_account_frozen_state():
    acc = Account(
        user_id="user-123",
        account_number="SF9999999999",
        balance=0.0,
        is_frozen=False
    )
    assert acc.is_frozen is False
    acc.is_frozen = True
    assert acc.is_frozen is True
