"""
Plans router – CRUD endpoints for subscription plans.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.plan import create_plan, delete_plan, get_plan, get_plans, update_plan
from app.database import get_db
from app.models.user import User
from app.schemas.plan import PlanCreate, PlanRead, PlanUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=list[PlanRead],
    summary="List plans",
    description="Return all available subscription plans.",
)
async def list_plans(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[PlanRead]:
    """Return a paginated list of subscription plans (public)."""
    return await get_plans(db, skip=skip, limit=limit)


@router.get(
    "/{plan_id}",
    response_model=PlanRead,
    summary="Get plan by ID",
    description="Return a single subscription plan.",
)
async def read_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PlanRead:
    """Return a plan by primary key (public)."""
    plan = await get_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found.",
        )
    return plan


@router.post(
    "/",
    response_model=PlanRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create plan",
    description="Create a new subscription plan. Requires authentication.",
)
async def create_plan_endpoint(
    plan_in: PlanCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> PlanRead:
    """Create a new subscription plan."""
    return await create_plan(db, plan_in)


@router.patch(
    "/{plan_id}",
    response_model=PlanRead,
    summary="Update plan",
    description="Partially update a subscription plan.",
)
async def update_plan_endpoint(
    plan_id: UUID,
    plan_in: PlanUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> PlanRead:
    """Update plan fields. Only provided fields are changed."""
    plan = await get_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found.",
        )
    return await update_plan(db, plan, plan_in)


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete plan",
    description="Permanently delete a subscription plan.",
)
async def delete_plan_endpoint(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a plan by primary key."""
    plan = await get_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found.",
        )
    await delete_plan(db, plan)
