class SentinelFlowException(Exception):
    """Base exception for all domain errors within SentinelFlow."""
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class AuthenticationError(SentinelFlowException):
    def __init__(self, message: str = "Invalid authentication credentials"):
        super().__init__(message, status_code=401)


class AuthorizationError(SentinelFlowException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class EntityNotFoundError(SentinelFlowException):
    def __init__(self, entity_name: str, identifier: str):
        super().__init__(f"{entity_name} with identifier '{identifier}' not found", status_code=404)


class InsufficientFundsError(SentinelFlowException):
    def __init__(self, account_id: str, current_balance: float, requested_amount: float):
        super().__init__(
            f"Account '{account_id}' has insufficient funds. Available: {current_balance}, Requested: {requested_amount}",
            status_code=422,
            details={"account_id": account_id, "available": current_balance, "requested": requested_amount}
        )


class FraudDetectedError(SentinelFlowException):
    def __init__(self, reason: str, risk_score: float):
        super().__init__(
            f"Transaction rejected due to fraud risk: {reason} (Score: {risk_score:.2f})",
            status_code=403,
            details={"reason": reason, "risk_score": risk_score}
        )


class IdempotencyConflictError(SentinelFlowException):
    def __init__(self, idempotency_key: str):
        super().__init__(
            f"Duplicate transaction request detected for idempotency key '{idempotency_key}'",
            status_code=409,
            details={"idempotency_key": idempotency_key}
        )


class RateLimitExceededError(SentinelFlowException):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            "API rate limit exceeded. Please throttle requests.",
            status_code=429,
            details={"retry_after_seconds": retry_after}
        )


class CircuitBreakerOpenError(SentinelFlowException):
    def __init__(self, service_name: str):
        super().__init__(
            f"Upstream service '{service_name}' is currently unavailable (circuit breaker OPEN).",
            status_code=503,
            details={"service": service_name}
        )
