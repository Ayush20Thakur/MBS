import pytest

@pytest.mark.asyncio
async def test_metrics_endpoint_response(client):
    res = await client.get("/api/v1/metrics")
    assert res.status_code == 200
    assert "sentinelflow_transactions_total" in res.text
