# SentinelFlow: Distributed Event-Driven Payment Ledger & Real-Time Fraud Engine

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SentinelFlow is a cloud-native, high-throughput financial transaction processing and anomaly detection platform designed for modern enterprise fintech infrastructure. It combines a mathematically rigorous double-entry ledger with a hybrid real-time fraud detection pipeline.

---

## 🏛️ System Architecture

```text
                             +------------------------+
                             |   Client Application   |
                             +-----------+------------+
                                         |
                                         | REST / HTTPS
                                         v
                             +------------------------+
                             |    FastAPI Gateway     |
                             |  - JWT Authentication  |
                             |  - Rate Limiter        |
                             |  - Idempotency Filter  |
                             +-----------+------------+
                                         |
                       +-----------------+-----------------+
                       |                                   |
                       v                                   v
        +-----------------------------+     +-----------------------------+
        |   Double-Entry Ledger Core  |     |   Hybrid Fraud Evaluator    |
        | - Immutable Journal Entries |     | - Sliding-Window Velocity   |
        | - Distributed Lock (Redlock)|     | - Geolocation Anomaly       |
        | - ACID Transaction State    |     | - Isolation Forest ML Score |
        +--------------+--------------+     +--------------+--------------+
                       |                                   |
                       +-----------------+-----------------+
                                         |
                                         v
                             +------------------------+
                             |  PostgreSQL / SQLite   |
                             |      Redis Cache       |
                             +------------------------+
```

---

## ⚡ Core Engineering Highlights

1. **Strict Double-Entry Bookkeeping**:
   - Zero-sum invariant: Every transaction requires balanced credit and debit ledger entries.
   - Prevents unbacked money creation and silent balance corruptions.

2. **Idempotency & Concurrency Control**:
   - Enforces unique client-supplied `Idempotency-Key` headers.
   - Distributed locking on account balances to prevent race conditions during rapid concurrent transfers.

3. **Hybrid Fraud Detection Pipeline**:
   - **Deterministic Heuristics**: Immediate rejection on exceeding velocity limits or single transaction thresholds.
   - **Machine Learning Anomaly Detection**: Unsupervised `IsolationForest` pipeline that computes dynamic risk scores (`0.0` to `1.0`).

4. **Resilience & Fault Tolerance**:
   - Built-in **Circuit Breaker** state machine (`CLOSED`, `OPEN`, `HALF-OPEN`) isolating external dependencies.
   - **Sliding-Window Rate Limiting** defending API endpoints against brute-force and DDoS patterns.

5. **Observability**:
   - Structured JSON logging with unified `X-Correlation-ID` request tracking.
   - Prometheus metrics exporter endpoint (`/metrics`) monitoring latency, transaction status, and fraud rates.

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- (Optional) Redis and PostgreSQL

### Installation
```bash
# Clone the repository
git clone https://github.com/Ayush20Thakur/MBS.git
cd MBS

# Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start server
uvicorn app.main:app --reload --port 8000
```

Access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Prometheus Metrics**: `http://localhost:8000/metrics`

---

## 📂 Repository Structure

```text
├── app/
│   ├── api/             # API routes & dependency injection
│   ├── core/            # Config, security, database, and telemetry
│   ├── models/          # SQLAlchemy ORM models (Accounts, Ledger, Fraud)
│   ├── schemas/         # Pydantic v2 validation contracts
│   ├── services/        # Ledger engine, Rule evaluator, ML scorer
│   └── main.py          # FastAPI application entrypoint
├── tests/               # Unit, integration, and load testing suites
├── docs/                # Architecture design & final year project report
├── .env.example         # Environment variable templates
├── requirements.txt     # Python package dependencies
└── README.md            # Project overview and documentation
```

---

## 📜 Academic Portfolio & Interview Defense
This project was engineered as a comprehensive Final Year B.Tech Computer Science Capstone Project addressing distributed concurrency, financial ledger integrity, and low-latency anomaly detection. See `docs/` for the complete IEEE-standard project report, design diagrams, and viva preparation guide.
