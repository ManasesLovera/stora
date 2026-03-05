"""
Invitations router – endpoints for creating and listing invitations.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.invitation import (
    create_invitation,
    delete_invitation,
    get_invitation,
    get_invitation_by_token,
    get_invitations_by_tenant,
)
from app.database import get_db
from app.models.user import User
from app.schemas.invitation import InvitationCreate, InvitationRead

router = APIRouter()


@router.get(
    "/tenant/{tenant_id}",
    response_model=list[InvitationRead],
    summary="List invitations by tenant",
    description="Return all invitations sent by a tenant.",
)
async def list_invitations(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[InvitationRead]:
    """Return invitations for a specific tenant."""
    return await get_invitations_by_tenant(db, tenant_id, skip=skip, limit=limit)


@router.get(
    "/{invitation_id}",
    response_model=InvitationRead,
    summary="Get invitation by ID",
    description="Return a single invitation.",
)
async def read_invitation(
    invitation_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> InvitationRead:
    """Return an invitation by primary key."""
    invitation = await get_invitation(db, invitation_id)
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found.",
        )
    return invitation


@router.get(
    "/token/{token}",
    response_model=InvitationRead,
    summary="Get invitation by token",
    description="Look up an invitation by its unique token (public endpoint).",
)
async def read_invitation_by_token(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> InvitationRead:
    """Return an invitation by token – used when an invitee clicks the link."""
    invitation = await get_invitation_by_token(db, token)
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found or expired.",
        )
    return invitation


@router.post(
    "/",
    response_model=InvitationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create invitation",
    description="Send an invitation to join a tenant.",
)
async def create_invitation_endpoint(
    invitation_in: InvitationCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> InvitationRead:
    """Create and return a new invitation."""
    return await create_invitation(db, invitation_in)


@router.delete(
    "/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete invitation",
    description="Revoke/delete an invitation.",
)
async def delete_invitation_endpoint(
    invitation_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete an invitation by primary key."""
    invitation = await get_invitation(db, invitation_id)
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found.",
        )
    await delete_invitation(db, invitation)
