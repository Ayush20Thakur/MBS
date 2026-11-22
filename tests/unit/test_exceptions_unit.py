import pytest
from app.core.exceptions import (
    SentinelFlowException,
    InsufficientFundsError,
    FraudDetectedError,
    IdempotencyConflictError
)

def test_exception_status_codes():
    insufficient = InsufficientFundsError("acc-1", 100.0, 200.0)
    assert insufficient.status_code == 422
    assert "insufficient funds" in insufficient.message.lower()

    fraud = FraudDetectedError("Velocity exceeded", 0.85)
    assert fraud.status_code == 403

    dup = IdempotencyConflictError("idem-key-1")
    assert dup.status_code == 409
