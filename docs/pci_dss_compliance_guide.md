# PCI-DSS Compliance & Security Blueprint

SentinelFlow is engineered to align with Payment Card Industry Data Security Standards (PCI-DSS v4.0):
1. **Primary Account Number (PAN) Protection**: No raw cardholder PANs are persisted in plaintext. All identities are referenced by synthetic UUID account tokens.
2. **Transmission Encryption**: Enforced TLS 1.3 across all client-to-gateway and internal service-to-service links.
3. **Immutable Audit Trails (Req 10)**: All ledger movements and administrative actions are logged with UTC timestamps and correlation IDs.
4. **Least Privilege RBAC (Req 7)**: Administrative capabilities strictly separated between Operators, Analysts, and End Customers.
