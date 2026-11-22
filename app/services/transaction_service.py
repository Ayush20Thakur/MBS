from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.transaction import Transaction, TransactionStatus
from app.models.fraud_incident import FraudIncident, IncidentStatus
from app.schemas.transaction import TransactionCreate
from app.services.account_service import AccountService
from app.services.ledger_service import LedgerService
from app.services.fraud_detector import FraudDetector
from app.services.ml_fraud_service import ml_fraud_service
from app.core.exceptions import (
    IdempotencyConflictError,
    FraudDetectedError,
    SentinelFlowException
)


class TransactionService:
    @classmethod
    async def process_transaction(
        cls,
        db: AsyncSession,
        payload: TransactionCreate
    ) -> Transaction:
        # 1. Idempotency Verification
        existing_tx = await db.execute(
            select(Transaction).where(Transaction.idempotency_key == payload.idempotency_key)
        )
        if existing_tx.scalar_one_or_none():
            raise IdempotencyConflictError(payload.idempotency_key)

        # 2. Retrieve Source & Destination Accounts
        source_account = await AccountService.get_account(db, payload.source_account_id)
        dest_account = await AccountService.get_account(db, payload.destination_account_id)

        if source_account.is_frozen:
            raise SentinelFlowException("Source account is frozen due to administrative hold.")
        if dest_account.is_frozen:
            raise SentinelFlowException("Destination account is frozen.")

        # 3. Hybrid Fraud Evaluation
        is_heuristic_fraud, rule_score, violations = await FraudDetector.evaluate_transaction(
            db=db,
            source_account_id=payload.source_account_id,
            amount=payload.amount,
            country_code=payload.country_code or "US"
        )
        ml_score = ml_fraud_service.compute_anomaly_score(
            amount=payload.amount,
            country_code=payload.country_code or "US"
        )

        composite_risk_score = round(max(rule_score, ml_score), 4)

        # 4. Initialize Transaction Entity
        transaction = Transaction(
            idempotency_key=payload.idempotency_key,
            source_account_id=payload.source_account_id,
            destination_account_id=payload.destination_account_id,
            amount=payload.amount,
            currency=payload.currency,
            risk_score=composite_risk_score,
            client_ip=payload.client_ip,
            country_code=payload.country_code,
            status=TransactionStatus.PROCESSING
        )
        db.add(transaction)
        await db.flush()

        # 5. Fraud Escalation or Execution
        if is_heuristic_fraud or composite_risk_score >= 0.75:
            transaction.status = TransactionStatus.REJECTED
            incident_reason = "; ".join(violations) if violations else f"High ML anomaly score ({ml_score:.2f})"
            incident = FraudIncident(
                transaction_id=transaction.id,
                risk_score=composite_risk_score,
                reasons=incident_reason,
                status=IncidentStatus.OPEN
            )
            db.add(incident)
            await db.commit()
            await db.refresh(transaction)
            raise FraudDetectedError(incident_reason, composite_risk_score)

        # 6. Execute Atomic Double-Entry Ledger Transfer
        await LedgerService.record_transfer(
            db=db,
            transaction=transaction,
            source=source_account,
            destination=dest_account,
            amount=payload.amount
        )

        transaction.status = TransactionStatus.SETTLED
        await db.commit()
        await db.refresh(transaction)
        return transaction
