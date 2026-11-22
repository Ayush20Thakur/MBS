# Production Troubleshooting & Operations Runbook

## 1. High Latency Alerts (P99 > 100ms)
- **Check**: Inspect PostgreSQL active connections: `SELECT count(*) FROM pg_stat_activity;`
- **Mitigate**: Verify Redis cache hit ratios. Restart lagging worker pods.

## 2. Circuit Breaker Trips OPEN
- **Check**: Inspect upstream banking gateway health endpoint.
- **Mitigate**: If upstream is degraded, circuit breaker will automatically transition to HALF-OPEN after 30 seconds.
