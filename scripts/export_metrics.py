import httpx
import asyncio

async def export():
    async with httpx.AsyncClient() as client:
        res = await client.get("http://localhost:8000/api/v1/metrics")
        print("Current Prometheus Exporter Metrics Snapshot:")
        print("=" * 60)
        for line in res.text.splitlines():
            if line.startswith("sentinelflow_"):
                print(line)

if __name__ == "__main__":
    asyncio.run(export())
