import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing_and_verification():
    raw_pwd = "SecureBankingPassword2026!"
    hashed = hash_password(raw_pwd)
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_jwt_token_encode_decode():
    data = {"sub": "user-uuid-1234", "role": "admin"}
    token = create_access_token(data)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "user-uuid-1234"
    assert decoded["role"] == "admin"
