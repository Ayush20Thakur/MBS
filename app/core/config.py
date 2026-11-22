from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelFlow"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    
    # Security & Auth
    SECRET_KEY: str = "sentinelflow-insecure-development-secret-key-32chars-min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Persistence
    DATABASE_URL: str = "sqlite+aiosqlite:///./sentinelflow.db"
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"

    # Risk Engine Rules
    VELOCITY_WINDOW_SECONDS: int = 60
    VELOCITY_MAX_TRANSACTIONS: int = 5
    MAX_SINGLE_TRANSACTION_LIMIT: float = 50000.00
    FRAUD_RISK_THRESHOLD: float = 0.75

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 120

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
