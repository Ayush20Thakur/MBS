import numpy as np
from datetime import datetime, timezone
from sklearn.ensemble import IsolationForest
from typing import Dict, Any


class MLFraudService:
    """
    Unsupervised Anomaly Detection using Isolation Forest to detect
    subtle multivariate fraudulent patterns in transaction feature space.
    """
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )
        self._is_trained = False
        self._bootstrap_synthetic_baseline()

    def _bootstrap_synthetic_baseline(self):
        """Pre-fit model on synthetic normal banking transaction distribution."""
        np.random.seed(42)
        # Features: [amount, hour_of_day, international_flag]
        normal_amounts = np.random.exponential(scale=120.0, size=(1000, 1))
        normal_hours = np.random.uniform(low=8, high=22, size=(1000, 1))
        normal_intl = np.random.binomial(n=1, p=0.08, size=(1000, 1))
        
        synthetic_normal_data = np.hstack([normal_amounts, normal_hours, normal_intl])
        self.model.fit(synthetic_normal_data)
        self._is_trained = True

    def extract_features(self, amount: float, country_code: str = "US") -> np.ndarray:
        now = datetime.now(timezone.utc)
        hour = now.hour
        is_international = 1.0 if country_code.upper() != "US" else 0.0
        return np.array([[amount, hour, is_international]])

    def compute_anomaly_score(self, amount: float, country_code: str = "US") -> float:
        """
        Calculates normalized risk score (0.0 to 1.0).
        Lower decision_function outputs indicate anomalous outliers.
        """
        features = self.extract_features(amount, country_code)
        raw_score = self.model.decision_function(features)[0]
        
        # Decision function: positive = normal, negative = anomaly
        # Map raw score (-0.5 to 0.5) to probability [0.0, 1.0]
        risk_score = 1.0 / (1.0 + np.exp(raw_score * 8.0))
        return float(np.clip(risk_score, 0.0, 1.0))


ml_fraud_service = MLFraudService()
