import unittest
import time

class BenchmarkScenarios(unittest.TestCase):
    def test_in_memory_rate_limiter_tps(self):
        from app.core.rate_limiter import SlidingWindowRateLimiter
        limiter = SlidingWindowRateLimiter(max_requests=10000, window_seconds=60)
        start = time.time()
        for i in range(1000):
            limiter.is_allowed("benchmark-client")
        elapsed = time.time() - start
        self.assertLess(elapsed, 0.5)

if __name__ == '__main__':
    unittest.main()
