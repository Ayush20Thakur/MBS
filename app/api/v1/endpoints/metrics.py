from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

router = APIRouter(tags=["System & Observability"])

# Prometheus Metrics
TRANSACTION_COUNTER = Counter(
    "sentinelflow_transactions_total",
    "Total count of processed transactions",
    ["status"]
)
FRAUD_COUNTER = Counter(
    "sentinelflow_fraud_detections_total",
    "Total count of rejected fraudulent transactions",
    ["reason"]
)
TRANSACTION_LATENCY = Histogram(
    "sentinelflow_transaction_processing_seconds",
    "Latency distribution of transaction execution in seconds",
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)


@router.get("/metrics")
async def get_prometheus_metrics():
    """Exports metrics in standard Prometheus text format."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get("/health")
async def health_check():
    """System liveness probe."""
    return {
        "status": "healthy",
        "service": "SentinelFlow",
        "version": "1.0.0"
    }
