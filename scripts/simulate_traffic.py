import asyncio
import httpx
import uuid
import random

BASE_URL = "http://localhost:8000/api/v1"

async def simulate():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Login
        login_res = await client.post("/auth/login", data={"username": "alice@fintech.io", "password": "AliceSecurePass123!"})
        if login_res.status_code != 200:
            print("Please run seed_demo_data.py first.")
            return
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Fetch accounts
        acc_res = await client.get("/accounts/", headers=headers)
        accounts = acc_res.json()
        if len(accounts) < 2:
            print("Need at least two accounts.")
            return

        acc_a = accounts[0]["id"]
        acc_b = accounts[1]["id"]

        print("Streaming simulated transactions...")
        for i in range(10):
            amount = round(random.uniform(10.0, 500.0), 2)
            payload = {
                "idempotency_key": str(uuid.uuid4()),
                "source_account_id": acc_a,
                "destination_account_id": acc_b,
                "amount": amount,
                "currency": "USD"
            }
            tx_res = await client.post("/transactions/", json=payload, headers=headers)
            print(f"Tx #{i+1}: Amount=${amount} -> Status: {tx_res.json().get('status', 'ERROR')}")
            await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(simulate())
