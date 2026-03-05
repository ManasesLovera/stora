"""
CRUD operations for the **Membership** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import Membership
from app.schemas.membership import MembershipCreate, MembershipUpdate


async def get_membership(db: AsyncSession, membership_id: UUID) -> Membership | None:
    """Return a single membership by primary key, or ``None``."""
    result = await db.execute(select(Membership).where(Membership.id == membership_id))
    return result.scalars().first()


async def get_memberships_by_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Membership]:
    """Return memberships for a given tenant."""
    result = await db.execute(
        select(Membership)
        .where(Membership.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_memberships_by_user(
    db: AsyncSession,
    user_id: UUID,
) -> list[Membership]:
    """Return all memberships for a given user."""
    result = await db.execute(select(Membership).where(Membership.user_id == user_id))
    return list(result.scalars().all())


async def create_membership(
    db: AsyncSession,
    membership_in: MembershipCreate,
) -> Membership:
    """Create a new membership."""
    membership = Membership(**membership_in.model_dump())
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership


async def update_membership(
    db: AsyncSession,
    membership: Membership,
    membership_in: MembershipUpdate,
) -> Membership:
    """Update an existing membership with the provided fields."""
    for field, value in membership_in.model_dump(exclude_unset=True).items():
        setattr(membership, field, value)

    await db.commit()
    await db.refresh(membership)
    return membership


async def delete_membership(db: AsyncSession, membership: Membership) -> None:
    """Delete a membership from the database."""
    await db.delete(membership)
    await db.commit()
