import asyncio
import uuid
from app.core.database import AsyncSessionLocal, init_db
from app.models.user import User, UserRole
from app.models.account import Account
from app.models.fraud_rule import FraudRule, RuleType, RuleAction
from app.core.security import hash_password

async def seed_data():
    await init_db()
    async with AsyncSessionLocal() as session:
        # Create Demo Admin
        admin = User(
            email="admin@sentinelflow.io",
            hashed_password=hash_password("AdminSecurePass123!"),
            full_name="Chief Risk Officer",
            role=UserRole.ADMIN
        )
        # Create Demo Customer
        alice = User(
            email="alice@fintech.io",
            hashed_password=hash_password("AliceSecurePass123!"),
            full_name="Alice Vance",
            role=UserRole.CUSTOMER
        )
        session.add_all([admin, alice])
        await session.flush()

        # Seed Accounts
        acc1 = Account(user_id=alice.id, account_number="SF1000000001", balance=15000.0, currency="USD")
        acc2 = Account(user_id=alice.id, account_number="SF1000000002", balance=2500.0, currency="USD")
        session.add_all([acc1, acc2])

        # Seed Core Fraud Rules
        rule1 = FraudRule(
            name="Max Single Wire Ceiling",
            description="Rejects any individual transaction greater than $50,000",
            rule_type=RuleType.AMOUNT_CEILING,
            threshold=50000.0,
            action=RuleAction.REJECT,
            is_active=True
        )
        rule2 = FraudRule(
            name="High-Risk Jurisdiction Sanction",
            description="Blocks transactions originating from sanctioned jurisdictions",
            rule_type=RuleType.COUNTRY_RESTRICTION,
            restriction_value="KP,IR,CU",
            action=RuleAction.REJECT,
            is_active=True
        )
        session.add_all([rule1, rule2])
        await session.commit()
        print("Database successfully seeded with users, accounts, and fraud rules.")

if __name__ == "__main__":
    asyncio.run(seed_data())
