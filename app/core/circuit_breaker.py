import time
import asyncio
from enum import Enum
from typing import Callable, Any
from app.core.exceptions import CircuitBreakerOpenError


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    """
    Production-grade circuit breaker to prevent cascading failures
    when communicating with upstream banking services or external APIs.
    """
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0,
        half_open_success_threshold: int = 2
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = time.time()
        self._lock = asyncio.Lock()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        async with self._lock:
            now = time.time()

            # Transition from OPEN to HALF_OPEN when recovery timeout has elapsed
            if self.state == CircuitState.OPEN:
                if now - self.last_state_change >= self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    self.last_state_change = now
                else:
                    raise CircuitBreakerOpenError(self.name)

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e

    async def _on_success(self):
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.half_open_success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.last_state_change = time.time()
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    async def _on_failure(self):
        async with self._lock:
            self.failure_count += 1
            if self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
                if self.failure_count >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
                    self.state = CircuitState.OPEN
                    self.last_state_change = time.time()
