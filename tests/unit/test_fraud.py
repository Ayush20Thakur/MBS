import pytest
import uuid
from app.services.fraud_detector import FraudDetector
from app.services.ml_fraud_service import ml_fraud_service


@pytest.mark.asyncio
async def test_fraud_detector_amount_ceiling(db_session):
    account_id = str(uuid.uuid4())
    # Test an amount exceeding the $50,000 threshold
    is_fraud, score, violations = await FraudDetector.evaluate_transaction(
        db=db_session,
        source_account_id=account_id,
        amount=75000.0,
        country_code="US"
    )

    assert is_fraud is True
    assert score >= 0.5
    assert any("exceeds hard limit" in v for v in violations)


def test_ml_anomaly_scoring_bounds():
    # Normal amount
    normal_score = ml_fraud_service.compute_anomaly_score(amount=50.0, country_code="US")
    assert 0.0 <= normal_score <= 1.0

    # Highly anomalous amount with international origin
    anomalous_score = ml_fraud_service.compute_anomaly_score(amount=990000.0, country_code="KP")
    assert 0.0 <= anomalous_score <= 1.0
    assert anomalous_score > normal_score
