import time
from collections import defaultdict
from typing import Dict, List
from app.core.exceptions import RateLimitExceededError


class SlidingWindowRateLimiter:
    """
    Sliding window log rate limiter maintaining microsecond-accurate
    request history to defend against burst traffic and abuse.
    """
    def __init__(self, max_requests: int = 120, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_logs: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        
        # Purge entries outside current sliding window
        self.request_logs[client_key] = [
            ts for ts in self.request_logs[client_key] if ts > window_start
        ]

        if len(self.request_logs[client_key]) >= self.max_requests:
            return False

        self.request_logs[client_key].append(now)
        return True

    def check(self, client_key: str):
        if not self.is_allowed(client_key):
            raise RateLimitExceededError(retry_after=self.window_seconds)


rate_limiter = SlidingWindowRateLimiter()
