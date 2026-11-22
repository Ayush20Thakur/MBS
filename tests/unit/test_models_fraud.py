import pytest
from app.models.fraud_incident import FraudIncident, IncidentStatus

def test_incident_resolution_status():
    inc = FraudIncident(
        transaction_id="tx-flagged",
        risk_score=0.88,
        reasons="Impossible travel across continents",
        status=IncidentStatus.OPEN
    )
    assert inc.status == IncidentStatus.OPEN
    inc.status = IncidentStatus.CONFIRMED_FRAUD
    assert inc.status == IncidentStatus.CONFIRMED_FRAUD
