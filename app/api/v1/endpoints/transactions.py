from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.api.deps import get_current_user, apply_rate_limit
from app.core.exceptions import EntityNotFoundError

router = APIRouter(prefix="/transactions", tags=["Transactions & Processing"])


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(apply_rate_limit)]
)
async def create_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ingests and processes a transaction with idempotency control,
    heuristic risk checks, ML anomaly scoring, and double-entry ledger execution.
    """
    transaction = await TransactionService.process_transaction(db=db, payload=payload)
    return transaction


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise EntityNotFoundError("Transaction", transaction_id)
    return transaction


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction).order_by(Transaction.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())
