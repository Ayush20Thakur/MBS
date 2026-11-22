from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.fraud_rule import FraudRule
from app.models.fraud_incident import FraudIncident
from app.schemas.fraud import (
    FraudRuleCreate,
    FraudRuleResponse,
    IncidentResponse,
    IncidentStatusUpdate
)
from app.api.deps import get_current_user, require_admin_user
from app.core.exceptions import EntityNotFoundError

router = APIRouter(prefix="/fraud", tags=["Fraud & Risk Management"])


@router.post("/rules", response_model=FraudRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_fraud_rule(
    payload: FraudRuleCreate,
    admin_user: User = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    rule = FraudRule(
        name=payload.name,
        description=payload.description,
        rule_type=payload.rule_type,
        threshold=payload.threshold,
        restriction_value=payload.restriction_value,
        action=payload.action,
        is_active=payload.is_active
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.get("/rules", response_model=List[FraudRuleResponse])
async def list_fraud_rules(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(FraudRule).order_by(FraudRule.created_at.desc()))
    return list(result.scalars().all())


@router.get("/incidents", response_model=List[IncidentResponse])
async def list_fraud_incidents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(FraudIncident).order_by(FraudIncident.created_at.desc()))
    return list(result.scalars().all())


@router.patch("/incidents/{incident_id}/status", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: str,
    payload: IncidentStatusUpdate,
    admin_user: User = Depends(require_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(FraudIncident).where(FraudIncident.id == incident_id))
    incident = result.scalar_one_or_none()
    if not incident:
        raise EntityNotFoundError("FraudIncident", incident_id)

    incident.status = payload.status
    incident.reviewed_by = admin_user.id
    await db.commit()
    await db.refresh(incident)
    return incident
