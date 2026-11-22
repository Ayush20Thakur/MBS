# System Data Dictionary

## Data Elements
- `idempotency_key`: 128-character unique string identifying a single intent to transfer funds.
- `balance_after`: Running snapshot of account balance immediately following journal entry application.
- `risk_score`: IEEE 754 floating point scalar $[0.0, 1.0]$ representing probability of fraudulent activity.
