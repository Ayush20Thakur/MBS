import asyncio
from app.core.database import AsyncSessionLocal
from app.services.ledger_service import LedgerService
from app.models.account import Account
from sqlalchemy import select

async def verify_all():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Account))
        accounts = res.scalars().all()
        print(f"Auditing ledger consistency across {len(accounts)} accounts...")
        for acc in accounts:
            audit = await LedgerService.audit_account_balance(session, acc.id)
            status = "BALANCED" if audit.is_balanced else "DISCREPANCY DETECTED"
            print(f"Account {acc.account_number}: Balance=${audit.account_balance} | Calc=${audit.calculated_balance} -> {status}")

if __name__ == "__main__":
    asyncio.run(verify_all())
