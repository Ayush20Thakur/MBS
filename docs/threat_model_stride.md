# Threat Model (STRIDE Methodology)

| Threat Category | Potential Attack Vector | SentinelFlow Countermeasure |
|---|---|---|
| **Spoofing** | Forged user identity tokens | Asymmetric HS256 JWT validation with expiration |
| **Tampering** | Balance alteration in transit | HTTPS TLS 1.3 + append-only ledger entries |
| **Repudiation** | Denying transaction dispatch | Client-supplied idempotency key + client IP logging |
| **Information Disclosure** | Leakage of account balances | Strict RBAC filtering |
| **Denial of Service** | Rapid request flooding | Sliding-window log rate limiting |
| **Elevation of Privilege** | Normal user calling admin endpoints | FastAPI dependency-injected role verification |
