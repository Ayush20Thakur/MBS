from datetime import datetime, timedelta, timezone
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.transaction import Transaction, TransactionStatus
from app.models.fraud_rule import FraudRule, RuleType, RuleAction
from app.core.config import settings


class FraudDetector:
    """
    Real-time deterministic fraud engine executing velocity checks,
    amount limits, and dynamic rule evaluations.
    """

    @classmethod
    async def evaluate_transaction(
        cls,
        db: AsyncSession,
        source_account_id: str,
        amount: float,
        country_code: str = "US"
    ) -> Tuple[bool, float, List[str]]:
        """
        Returns (is_fraudulent, risk_score, list_of_violations).
        Risk score scaled from 0.0 (safe) to 1.0 (critical fraud).
        """
        violations = []
        base_risk_score = 0.0

        # 1. Hard Amount Ceiling Check
        if amount > settings.MAX_SINGLE_TRANSACTION_LIMIT:
            violations.append(f"Transaction amount {amount} exceeds hard limit {settings.MAX_SINGLE_TRANSACTION_LIMIT}")
            base_risk_score += 0.50

        # 2. Sliding Window Velocity Check
        window_start = datetime.now(timezone.utc) - timedelta(seconds=settings.VELOCITY_WINDOW_SECONDS)
        velocity_query = select(func.count(Transaction.id)).where(
            Transaction.source_account_id == source_account_id,
            Transaction.created_at >= window_start
        )
        velocity_res = await db.execute(velocity_query)
        recent_count = velocity_res.scalar() or 0

        if recent_count >= settings.VELOCITY_MAX_TRANSACTIONS:
            violations.append(f"Velocity exceeded: {recent_count} transactions in {settings.VELOCITY_WINDOW_SECONDS}s")
            base_risk_score += 0.40

        # 3. Dynamic Rule Evaluation from Database
        rules_query = select(FraudRule).where(FraudRule.is_active == True)
        rules_res = await db.execute(rules_query)
        active_rules = rules_res.scalars().all()

        for rule in active_rules:
            if rule.rule_type == RuleType.AMOUNT_CEILING and rule.threshold:
                if amount > rule.threshold:
                    violations.append(f"Triggered rule '{rule.name}': Amount {amount} > {rule.threshold}")
                    base_risk_score += 0.35
            elif rule.rule_type == RuleType.COUNTRY_RESTRICTION and rule.restriction_value:
                restricted_countries = [c.strip().upper() for c in rule.restriction_value.split(",")]
                if country_code.upper() in restricted_countries:
                    violations.append(f"Triggered rule '{rule.name}': High-risk origin country '{country_code}'")
                    base_risk_score += 0.45

        normalized_score = min(base_risk_score, 1.0)
        is_fraud = normalized_score >= settings.FRAUD_RISK_THRESHOLD or len(violations) > 0

        return is_fraud, normalized_score, violations
