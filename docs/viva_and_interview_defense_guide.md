# SentinelFlow: College Viva Defense & SDE Interview Technical Guide

This document prepares you for technical interviews and external college project defense examinations.

---

### Q1: Why did you choose double-entry bookkeeping over a simple `balance` column update?
**Answer:**
A simple `balance` update (e.g. `UPDATE accounts SET balance = balance - 100`) is vulnerable to silent corruption, partial failure anomalies, and lack of auditability. If a node crashes mid-transaction or a race condition occurs, tracking where funds vanished is impossible.
With **Double-Entry Bookkeeping**:
1. Every economic movement produces two balanced journal entries: one `DEBIT` and one matching `CREDIT`.
2. Entries are strictly append-only (immutable).
3. The system enforces a zero-sum invariant: $\sum \text{Debits} = \sum \text{Credits}$. At any point, the auditor can calculate $\sum \text{Credits} - \sum \text{Debits}$ to reconstruct the exact balance and verify ledger integrity mathematically.

---

### Q2: How does the system handle duplicate payment requests when a user clicks 'Pay' twice or suffers a network timeout?
**Answer:**
We implement **Idempotency Control** using client-generated `Idempotency-Key` headers (typically UUIDv4):
1. When a transaction request arrives, the system queries the database for an existing record with that `idempotency_key`.
2. If found, the orchestrator detects the conflict and rejects the duplicate with HTTP `409 Conflict` (or returns the previously cached response if already completed).
3. The database enforces a `UNIQUE` B-tree constraint on `idempotency_key`, guaranteeing that even concurrent racing requests cannot write duplicate ledger transfers.

---

### Q3: What are the CAP Theorem trade-offs made in SentinelFlow?
**Answer:**
In financial ledger systems, **Consistency (C)** and **Partition Tolerance (P)** are prioritized over raw Write Availability (A) — making SentinelFlow a **CP system**:
- In the presence of a network partition between database nodes, the system halts writes or requires quorum rather than permitting "split-brain" balance updates that could generate unbacked currency.
- Financial correctness always supersedes momentary downtime.

---

### Q4: Why use Isolation Forest for fraud detection instead of a supervised classifier like Random Forest or XGBoost?
**Answer:**
In production financial fraud:
1. **Severe Class Imbalance**: Fraud typically constitutes < 0.1% of all transactions.
2. **Evolving Attack Vectors (Zero-Day Fraud)**: Fraudsters constantly modify techniques. Supervised models trained on historical fraud labels fail to detect novel attack patterns.
3. **Isolation Forest** is an unsupervised anomaly detection algorithm based on recursive partitioning. Because anomalies are "few and different", they require significantly fewer tree splits to isolate from normal data points. This makes it effective at flagging novel, high-risk outliers without requiring pre-labeled fraud datasets.

---

### Q5: How does your Circuit Breaker protect the system?
**Answer:**
The Circuit Breaker pattern isolates slow or failing external services (e.g., third-party banking APIs, SMS gateways):
1. **CLOSED**: Normal state. Calls pass through. Failures are counted.
2. **OPEN**: When failures cross the threshold (e.g., 5 consecutive failures), the breaker trips OPEN. Calls fail immediately without hitting the network, preventing thread pool exhaustion and cascading timeouts.
3. **HALF-OPEN**: After a recovery timeout (e.g., 30s), a probe request tests upstream health. If successful, the breaker resets to CLOSED; if it fails, it trips back to OPEN.

---

### Q6: What is the difference between Fixed-Window and Sliding-Window Rate Limiting?
**Answer:**
- **Fixed-Window**: Counts requests in fixed time buckets (e.g., 00:00 to 00:01). Vulnerable to "bursting at window boundaries", where an attacker sends maximum quota at 00:59 and another maximum quota at 01:00, effectively doubling the allowed throughput.
- **Sliding-Window Log**: Maintains timestamps of each request. For any incoming request at timestamp $t$, it purges timestamps $< t - \text{window}$ and verifies whether the remaining count is within quota. This guarantees smooth rate enforcement across any moving window.

---

### Q7: What database isolation level is required for the financial transfer transaction?
**Answer:**
We require **`SERIALIZABLE`** or **`REPEATABLE READ` with row-level pessimistic locking (`SELECT ... FOR UPDATE`)**.
Standard `READ COMMITTED` allows race conditions where two concurrent threads check `balance >= 100` simultaneously, both see $150 available, and both deduct $100, leaving the account in an illegal negative overdraft ($50 deficit). Row-level locking ensures only one transaction mutates the source balance at a time.
