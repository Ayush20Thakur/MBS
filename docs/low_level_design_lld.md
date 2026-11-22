# Low-Level Design (LLD): SentinelFlow

## 1. Class Design and Data Contracts
### 1.1 Double-Entry Transaction Ledger Flow
```python
async def record_transfer(db, transaction, source, destination, amount):
    # 1. Assert balance sufficiency: source.balance >= amount
    # 2. Debit source: source.balance -= amount
    # 3. Credit destination: destination.balance += amount
    # 4. Assert zero-sum balance: sum(debit) == sum(credit)
    # 5. Atomic database flush
```

### 1.2 Isolation Forest Anomaly Scoring
```python
features = [amount, hour_of_day, is_international]
raw_score = model.decision_function(features)[0]
risk_score = 1.0 / (1.0 + exp(raw_score * 8.0))
```
