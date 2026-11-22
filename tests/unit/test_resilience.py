import pytest
import asyncio
from app.core.circuit_breaker import CircuitBreaker, CircuitState
from app.core.exceptions import CircuitBreakerOpenError
from app.core.rate_limiter import SlidingWindowRateLimiter


@pytest.mark.asyncio
async def test_circuit_breaker_transitions():
    cb = CircuitBreaker("upstream-payment-mock", failure_threshold=2, recovery_timeout_seconds=0.1)

    async def faulty_upstream():
        raise ConnectionResetError("Remote server disconnected")

    # 1st failure
    with pytest.raises(ConnectionResetError):
        await cb.call(faulty_upstream)
    assert cb.state == CircuitState.CLOSED

    # 2nd failure triggers OPEN
    with pytest.raises(ConnectionResetError):
        await cb.call(faulty_upstream)
    assert cb.state == CircuitState.OPEN

    # Subsequent call rejected immediately without executing faulty_upstream
    with pytest.raises(CircuitBreakerOpenError):
        await cb.call(faulty_upstream)

    # Wait for recovery timeout
    await asyncio.sleep(0.12)

    # Next call transitions to HALF_OPEN
    async def healthy_upstream():
        return {"status": "ok"}

    result = await cb.call(healthy_upstream)
    assert result == {"status": "ok"}


def test_rate_limiter_sliding_window():
    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=10)
    client_ip = "192.168.1.100"

    assert limiter.is_allowed(client_ip) is True
    assert limiter.is_allowed(client_ip) is True
    # 3rd request in same window rejected
    assert limiter.is_allowed(client_ip) is False
