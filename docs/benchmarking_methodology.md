# Benchmarking & Stress Methodology

## Testing Environment
- 4-core, 16GB RAM virtualized test bench.
- PostgreSQL 16 on NVMe SSD storage.
- In-memory SQLite async test harness for deterministic micro-benchmarks.

## Test Matrix
1. **Normal Flow**: 10,000 requests @ 200 concurrent users.
2. **Velocity Spike**: 500 requests dispatched within a 2-second burst from a single account.
3. **Idempotency Contention**: 50 concurrent threads submitting identical idempotency keys.
