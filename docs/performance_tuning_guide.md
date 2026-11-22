# Performance Tuning & Optimization Guide

## 1. Database Connection Pooling
- Configure SQLAlchemy `pool_size=20`, `max_overflow=10` per pod.
- Enable `pool_pre_ping=True` in production to prevent stale connection timeouts.

## 2. Uvicorn Worker Scaling
- Recommended worker formula: `workers = (2 * CPU_CORES) + 1`.
- Use uvloop for ultra-high-throughput Linux production deployments.
