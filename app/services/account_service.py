import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.account import Account
from app.core.exceptions import EntityNotFoundError


class AccountService:
    @staticmethod
    def _generate_account_number() -> str:
        """Generate pseudo-random standardized 12-digit account number."""
        return f"SF{random.randint(1000000000, 9999999999)}"

    @classmethod
    async def create_account(
        cls,
        db: AsyncSession,
        user_id: str,
        currency: str = "USD",
        initial_deposit: float = 0.0
    ) -> Account:
        account = Account(
            user_id=user_id,
            account_number=cls._generate_account_number(),
            currency=currency.upper(),
            balance=initial_deposit
        )
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account

    @classmethod
    async def get_account(cls, db: AsyncSession, account_id: str) -> Account:
        result = await db.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        if not account:
            raise EntityNotFoundError("Account", account_id)
        return account

    @classmethod
    async def get_user_accounts(cls, db: AsyncSession, user_id: str) -> List[Account]:
        result = await db.execute(select(Account).where(Account.user_id == user_id))
        return list(result.scalars().all())

    @classmethod
    async def deposit(cls, db: AsyncSession, account_id: str, amount: float) -> Account:
        account = await cls.get_account(db, account_id)
        account.balance += amount
        await db.commit()
        await db.refresh(account)
        return account
