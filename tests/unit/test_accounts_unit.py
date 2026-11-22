import pytest
import uuid
from app.services.account_service import AccountService
from app.models.account import Account

@pytest.mark.asyncio
async def test_account_creation_and_deposit(db_session):
    user_id = str(uuid.uuid4())
    account = await AccountService.create_account(db_session, user_id, "USD", 500.0)
    assert account.balance == 500.0
    assert account.currency == "USD"
    assert account.account_number.startswith("SF")

    updated = await AccountService.deposit(db_session, account.id, 250.0)
    assert updated.balance == 750.0
