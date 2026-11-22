import pytest
from app.models.user import User, UserRole

def test_user_entity_defaults():
    user = User(
        email="test@user.com",
        hashed_password="hashed_pwd_string",
        full_name="Test User",
        is_active=True
    )
    assert user.email == "test@user.com"
    assert user.is_active is True
