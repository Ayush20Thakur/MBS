import pytest
from app.core.circuit_breaker import CircuitBreaker, CircuitState

@pytest.mark.asyncio
async def test_circuit_breaker_recovery():
    cb = CircuitBreaker("mock-service", failure_threshold=1, recovery_timeout_seconds=0.05)
    async def fail(): raise RuntimeError("fail")
    with pytest.raises(RuntimeError):
        await cb.call(fail)
    assert cb.state == CircuitState.OPEN
