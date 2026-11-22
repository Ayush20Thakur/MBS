import pytest

@pytest.mark.asyncio
async def test_health_check_payload(client):
    res = await client.get("/api/v1/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "healthy"
    assert body["service"] == "SentinelFlow"
