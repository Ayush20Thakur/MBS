# Distributed Consensus & Fault Tolerance

## 1. Distributed Locking via Redlock
To prevent concurrent race conditions on account balances:
- The orchestrator acquires a distributed lock on the account UUID with a 5000ms TTL.
- Ensures strict serializability even when multiple API gateway pods concurrently process transactions for the same account.

## 2. Split-Brain Mitigation
Under network partitions, SentinelFlow adheres to the CAP theorem by favoring Consistency over Write Availability (CP). Writes are halted if quorum cannot be validated.
