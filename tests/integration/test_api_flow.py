import pytest
import uuid


@pytest.mark.asyncio
async def test_full_system_lifecycle(client):
    # 1. Register User
    user_payload = {
        "email": "ayush.thakur@example.com",
        "password": "Password123!",
        "full_name": "Ayush Thakur",
        "role": "admin"
    }
    reg_res = await client.post("/api/v1/auth/register", json=user_payload)
    assert reg_res.status_code == 201

    # 2. Login
    login_data = {"username": user_payload["email"], "password": user_payload["password"]}
    login_res = await client.post("/api/v1/auth/login", data=login_data)
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Two Accounts
    acc1_res = await client.post(
        "/api/v1/accounts/",
        json={"currency": "USD", "initial_deposit": 1000.0},
        headers=auth_headers
    )
    assert acc1_res.status_code == 201
    acc1_id = acc1_res.json()["id"]

    acc2_res = await client.post(
        "/api/v1/accounts/",
        json={"currency": "USD", "initial_deposit": 0.0},
        headers=auth_headers
    )
    assert acc2_res.status_code == 201
    acc2_id = acc2_res.json()["id"]

    # 4. Execute Valid Ledger Transfer ($300 from acc1 to acc2)
    idempotency_key = str(uuid.uuid4())
    tx_payload = {
        "idempotency_key": idempotency_key,
        "source_account_id": acc1_id,
        "destination_account_id": acc2_id,
        "amount": 300.0,
        "currency": "USD"
    }
    tx_res = await client.post("/api/v1/transactions/", json=tx_payload, headers=auth_headers)
    assert tx_res.status_code == 201
    assert tx_res.json()["status"] == "SETTLED"

    # 5. Verify Idempotency Protection (Duplicate Submission)
    dup_res = await client.post("/api/v1/transactions/", json=tx_payload, headers=auth_headers)
    assert dup_res.status_code == 409

    # 6. Audit Double-Entry Balance Integrity
    audit_res = await client.get(f"/api/v1/accounts/{acc1_id}/audit", headers=auth_headers)
    assert audit_res.status_code == 200

    # 7. Attempt Fraudulent Transaction Exceeding Threshold ($80,000)
    fraud_payload = {
        "idempotency_key": str(uuid.uuid4()),
        "source_account_id": acc1_id,
        "destination_account_id": acc2_id,
        "amount": 80000.0,
        "currency": "USD"
    }
    fraud_res = await client.post("/api/v1/transactions/", json=fraud_payload, headers=auth_headers)
    assert fraud_res.status_code == 403
    assert "FraudDetectedError" in fraud_res.json()["error"]
