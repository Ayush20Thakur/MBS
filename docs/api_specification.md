# OpenAPI REST Interface Specification

## Endpoints Summary
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Register new user account | None |
| POST | `/api/v1/auth/login` | Authenticate and obtain JWT | None |
| GET | `/api/v1/accounts/` | List user accounts | Bearer JWT |
| POST | `/api/v1/accounts/` | Open new ledger account | Bearer JWT |
| POST | `/api/v1/transactions/` | Ingest idempotent payment | Bearer JWT |
| GET | `/api/v1/accounts/{id}/audit` | Reconcile double-entry ledger | Bearer JWT |
| GET | `/api/v1/fraud/incidents` | Query open risk cases | Bearer (Analyst/Admin) |
| GET | `/api/v1/metrics` | Prometheus metrics exporter | None |
| GET | `/api/v1/health` | Service liveness probe | None |
