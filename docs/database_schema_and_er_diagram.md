# SentinelFlow: Database Schema & Entity-Relationship Specification

## 1. Entity-Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ ACCOUNT : "owns"
    ACCOUNT ||--o{ TRANSACTION : "source_of"
    ACCOUNT ||--o{ TRANSACTION : "destination_of"
    ACCOUNT ||--o{ LEDGER_ENTRY : "has_entries"
    TRANSACTION ||--o{ LEDGER_ENTRY : "generates"
    TRANSACTION ||--o| FRAUD_INCIDENT : "flags"

    USER {
        string id PK
        string email UK
        string hashed_password
        string full_name
        string role
        boolean is_active
        datetime created_at
    }

    ACCOUNT {
        string id PK
        string user_id FK
        string account_number UK
        string currency
        float balance
        boolean is_frozen
        datetime created_at
    }

    TRANSACTION {
        string id PK
        string idempotency_key UK
        string source_account_id FK
        string destination_account_id FK
        float amount
        string currency
        string status
        float risk_score
        string client_ip
        string country_code
        datetime created_at
        datetime updated_at
    }

    LEDGER_ENTRY {
        string id PK
        string transaction_id FK
        string account_id FK
        string entry_type
        float amount
        float balance_after
        datetime created_at
    }

    FRAUD_RULE {
        string id PK
        string name UK
        string description
        string rule_type
        float threshold
        string restriction_value
        string action
        boolean is_active
        datetime created_at
    }

    FRAUD_INCIDENT {
        string id PK
        string transaction_id FK,UK
        float risk_score
        text reasons
        string status
        string reviewed_by
        datetime created_at
        datetime updated_at
    }
```

---

## 2. Table Specifications and Invariants

### 2.1 `transactions` Table
- **Index**: Unique B-tree index on `idempotency_key`.
- **Foreign Keys**: `source_account_id -> accounts(id)`, `destination_account_id -> accounts(id)`.
- **Constraint**: `amount > 0.0`.

### 2.2 `ledger_entries` Table
- **Immutability**: No `UPDATE` or `DELETE` operations are ever performed on this table.
- **Audit Invariant**: For every completed transaction $T$, $\sum \text{Debit}(T) = \sum \text{Credit}(T) = \text{Amount}(T)$.
- **Account Reconciliation**: $\text{Balance}(A) = \sum \text{Credit}(A) - \sum \text{Debit}(A) + \text{InitialBalance}(A)$.

### 2.3 `fraud_incidents` Table
- Tracks investigation lifecycle for rejected or flagged transactions.
- Provides compliance audit trail for financial regulators.
