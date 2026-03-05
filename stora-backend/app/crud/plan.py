"""
CRUD operations for the **Plan** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate


async def get_plan(db: AsyncSession, plan_id: UUID) -> Plan | None:
    """Return a single plan by primary key, or ``None``."""
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    return result.scalars().first()


async def get_plans(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[Plan]:
    """Return a paginated list of plans."""
    result = await db.execute(select(Plan).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_plan(db: AsyncSession, plan_in: PlanCreate) -> Plan:
    """Create a new subscription plan."""
    plan = Plan(**plan_in.model_dump())
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


async def update_plan(
    db: AsyncSession,
    plan: Plan,
    plan_in: PlanUpdate,
) -> Plan:
    """Update an existing plan with the provided fields."""
    for field, value in plan_in.model_dump(exclude_unset=True).items():
        setattr(plan, field, value)

    await db.commit()
    await db.refresh(plan)
    return plan


async def delete_plan(db: AsyncSession, plan: Plan) -> None:
    """Delete a plan from the database."""
    await db.delete(plan)
    await db.commit()
