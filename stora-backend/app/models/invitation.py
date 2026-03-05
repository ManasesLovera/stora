"""
Invitation model – tracks pending invitations sent by a tenant to
prospective team members via e-mail.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Invitation(Base):
    """
    An invitation for a person to join a tenant with a specific role.

    Attributes:
        id:         Unique identifier (UUID).
        tenant_id:  FK → tenants.id – the tenant sending the invite.
        email:      E-mail address of the invitee.
        role:       Role to assign upon acceptance.
        token:      Unique token embedded in the invitation link.
        expires_at: Expiry timestamp after which the invite is invalid.
    """

    __tablename__ = "invitations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
        comment="FK → tenants.id – tenant that sent the invitation.",
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Invitee e-mail address.",
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="staff",
        comment="Role to assign: owner, co_owner, admin, or staff.",
    )
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="Unique token used in the invitation link.",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Timestamp when this invitation expires.",
    )

    # ── Relationships ────────────────────────────────────────
    tenant = relationship("Tenant", back_populates="invitations")
