import pytest
from app.core.rate_limiter import SlidingWindowRateLimiter

def test_sliding_window_burst_mitigation():
    limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=1)
    ip = "10.0.0.1"
    for _ in range(5):
        assert limiter.is_allowed(ip) is True
    assert limiter.is_allowed(ip) is False
