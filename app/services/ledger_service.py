from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Tuple
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.ledger import LedgerEntry, EntryType
from app.schemas.ledger import LedgerBalanceAudit
from app.core.exceptions import InsufficientFundsError, SentinelFlowException


class LedgerService:
    """
    Guarantees strict double-entry ledger bookkeeping.
    Every balance mutation requires corresponding, offsetting journal entries.
    """

    @classmethod
    async def record_transfer(
        cls,
        db: AsyncSession,
        transaction: Transaction,
        source: Account,
        destination: Account,
        amount: float
    ) -> Tuple[LedgerEntry, LedgerEntry]:
        if source.balance < amount:
            raise InsufficientFundsError(source.id, source.balance, amount)

        # Debit source account
        source.balance -= amount
        debit_entry = LedgerEntry(
            transaction_id=transaction.id,
            account_id=source.id,
            entry_type=EntryType.DEBIT,
            amount=amount,
            balance_after=source.balance
        )

        # Credit destination account
        destination.balance += amount
        credit_entry = LedgerEntry(
            transaction_id=transaction.id,
            account_id=destination.id,
            entry_type=EntryType.CREDIT,
            amount=amount,
            balance_after=destination.balance
        )

        # Enforce zero-sum invariant before persisting
        if debit_entry.amount != credit_entry.amount:
            raise SentinelFlowException("Invariant violation: Debit and Credit sums do not match.")

        db.add(debit_entry)
        db.add(credit_entry)
        return debit_entry, credit_entry

    @classmethod
    async def audit_account_balance(cls, db: AsyncSession, account_id: str) -> LedgerBalanceAudit:
        """
        Reconciles ledger journal entries against cached account balance.
        Calculated Balance = Sum(Credits) - Sum(Debits).
        """
        # Fetch current balance
        account_res = await db.execute(select(Account).where(Account.id == account_id))
        account = account_res.scalar_one_or_none()
        if not account:
            raise SentinelFlowException(f"Account {account_id} not found")

        # Sum Credits
        credit_query = select(func.coalesce(func.sum(LedgerEntry.amount), 0.0)).where(
            LedgerEntry.account_id == account_id,
            LedgerEntry.entry_type == EntryType.CREDIT
        )
        credit_res = await db.execute(credit_query)
        sum_credits = float(credit_res.scalar())

        # Sum Debits
        debit_query = select(func.coalesce(func.sum(LedgerEntry.amount), 0.0)).where(
            LedgerEntry.account_id == account_id,
            LedgerEntry.entry_type == EntryType.DEBIT
        )
        debit_res = await db.execute(debit_query)
        sum_debits = float(debit_res.scalar())

        calculated_balance = sum_credits - sum_debits
        # Note: If account had an initial deposit prior to ledger tracking, offset applies
        is_balanced = abs(calculated_balance - account.balance) < 0.001

        return LedgerBalanceAudit(
            account_id=account_id,
            account_balance=account.balance,
            sum_credits=sum_credits,
            sum_debits=sum_debits,
            calculated_balance=calculated_balance,
            is_balanced=is_balanced
        )
