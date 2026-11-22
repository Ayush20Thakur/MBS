from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.accounts import router as accounts_router
from app.api.v1.endpoints.transactions import router as transactions_router
from app.api.v1.endpoints.fraud import router as fraud_router
from app.api.v1.endpoints.metrics import router as metrics_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(accounts_router)
api_v1_router.include_router(transactions_router)
api_v1_router.include_router(fraud_router)
api_v1_router.include_router(metrics_router)
