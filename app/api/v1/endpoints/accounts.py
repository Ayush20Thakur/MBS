from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse, DepositRequest
from app.schemas.ledger import LedgerBalanceAudit
from app.services.account_service import AccountService
from app.services.ledger_service import LedgerService
from app.api.deps import get_current_user

router = APIRouter(prefix="/accounts", tags=["Accounts & Ledger"])


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    payload: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await AccountService.create_account(
        db=db,
        user_id=current_user.id,
        currency=payload.currency,
        initial_deposit=payload.initial_deposit
    )
    return account


@router.get("/", response_model=List[AccountResponse])
async def list_user_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.get_user_accounts(db, current_user.id)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account_detail(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.get_account(db, account_id)


@router.post("/{account_id}/deposit", response_model=AccountResponse)
async def deposit_funds(
    account_id: str,
    payload: DepositRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.deposit(db, account_id, payload.amount)


@router.get("/{account_id}/audit", response_model=LedgerBalanceAudit)
async def audit_account_ledger(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Reconciles and verifies mathematical balance across all journal entries."""
    return await LedgerService.audit_account_balance(db, account_id)
