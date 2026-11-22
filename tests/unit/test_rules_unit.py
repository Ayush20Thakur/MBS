import pytest
from app.models.fraud_rule import FraudRule, RuleType, RuleAction

def test_fraud_rule_model_instantiation():
    rule = FraudRule(
        name="Test Velocity Limit",
        rule_type=RuleType.VELOCITY_COUNT,
        threshold=10.0,
        action=RuleAction.FLAG,
        is_active=True
    )
    assert rule.name == "Test Velocity Limit"
    assert rule.action == RuleAction.FLAG
    assert rule.is_active is True
