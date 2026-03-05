"""
Memberships router – CRUD endpoints for tenant memberships.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.membership import (
    create_membership,
    delete_membership,
    get_membership,
    get_memberships_by_tenant,
    update_membership,
)
from app.database import get_db
from app.models.user import User
from app.schemas.membership import MembershipCreate, MembershipRead, MembershipUpdate

router = APIRouter()


@router.get(
    "/tenant/{tenant_id}",
    response_model=list[MembershipRead],
    summary="List memberships by tenant",
    description="Return memberships for a specific tenant.",
)
async def list_memberships(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[MembershipRead]:
    """Return all memberships for a tenant."""
    return await get_memberships_by_tenant(db, tenant_id, skip=skip, limit=limit)


@router.get(
    "/{membership_id}",
    response_model=MembershipRead,
    summary="Get membership by ID",
    description="Return a single membership.",
)
async def read_membership(
    membership_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> MembershipRead:
    """Return a membership by primary key."""
    membership = await get_membership(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )
    return membership


@router.post(
    "/",
    response_model=MembershipRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create membership",
    description="Link a user to a tenant with a specific role.",
)
async def create_membership_endpoint(
    membership_in: MembershipCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> MembershipRead:
    """Create a new membership."""
    return await create_membership(db, membership_in)


@router.patch(
    "/{membership_id}",
    response_model=MembershipRead,
    summary="Update membership",
    description="Update the role or status of a membership.",
)
async def update_membership_endpoint(
    membership_id: UUID,
    membership_in: MembershipUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> MembershipRead:
    """Update membership fields."""
    membership = await get_membership(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )
    return await update_membership(db, membership, membership_in)


@router.delete(
    "/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete membership",
    description="Remove a user from a tenant.",
)
async def delete_membership_endpoint(
    membership_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a membership by primary key."""
    membership = await get_membership(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )
    await delete_membership(db, membership)
