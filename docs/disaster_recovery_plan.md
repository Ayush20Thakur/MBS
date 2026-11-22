# Disaster Recovery & Business Continuity Plan (BCP)

## 1. Recovery Point Objective (RPO)
- **Target**: RPO < 5 seconds.
- **Mechanism**: Continuous PostgreSQL WAL (Write-Ahead Logging) replication to secondary AWS availability zones.

## 2. Recovery Time Objective (RTO)
- **Target**: RTO < 60 seconds.
- **Mechanism**: Automated Kubernetes Horizontal Pod Autoscaler and StatefulSet volume failover.
