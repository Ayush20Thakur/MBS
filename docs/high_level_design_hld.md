# High-Level Design (HLD): SentinelFlow

## 1. Architectural Strategy
SentinelFlow utilizes an event-driven, decoupled microservices topology:
- **API Ingestion Gateway**: Built with asynchronous Python (FastAPI/Uvicorn), enforcing non-blocking event loops.
- **Ledger Kernel**: Maintains ACID guarantees via strict double-entry accounting.
- **Risk Assessment Mesh**: Evaluates incoming transaction vectors against heuristic sliding windows and machine learning models.
- **State & Caching Subsystem**: Redis in-memory cache for sliding-window log tracking and distributed lock coordination.
- **Relational Persistence**: PostgreSQL with row-level locks and append-only ledger entries.
