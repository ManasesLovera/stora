"""
CRUD operations for the **Invitation** model.
"""

import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invitation import Invitation
from app.schemas.invitation import InvitationCreate


async def get_invitation(db: AsyncSession, invitation_id: UUID) -> Invitation | None:
    """Return a single invitation by primary key, or ``None``."""
    result = await db.execute(
        select(Invitation).where(Invitation.id == invitation_id)
    )
    return result.scalars().first()


async def get_invitation_by_token(db: AsyncSession, token: str) -> Invitation | None:
    """Return an invitation by its unique token, or ``None``."""
    result = await db.execute(
        select(Invitation).where(Invitation.token == token)
    )
    return result.scalars().first()


async def get_invitations_by_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Invitation]:
    """Return invitations for a given tenant."""
    result = await db.execute(
        select(Invitation)
        .where(Invitation.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_invitation(
    db: AsyncSession,
    invitation_in: InvitationCreate,
    expires_in_hours: int = 48,
) -> Invitation:
    """
    Create a new invitation.

    Automatically generates a secure token and sets the expiry timestamp.
    """
    invitation = Invitation(
        tenant_id=invitation_in.tenant_id,
        email=invitation_in.email,
        role=invitation_in.role,
        token=secrets.token_urlsafe(32),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=expires_in_hours),
    )
    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)
    return invitation


async def delete_invitation(db: AsyncSession, invitation: Invitation) -> None:
    """Delete an invitation from the database."""
    await db.delete(invitation)
    await db.commit()
