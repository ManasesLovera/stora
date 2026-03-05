"""
Membership model – links a User to a Tenant with a specific role,
implementing role-based access control (RBAC).
"""

import uuid

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Membership(Base):
    """
    A user's membership within a tenant, defining their role.

    Attributes:
        id:        Unique identifier (UUID).
        user_id:   FK → users.id.
        tenant_id: FK → tenants.id.
        role:      One of 'owner', 'co_owner', 'admin', 'staff'.
        status:    'active' or 'suspended'.
    """

    __tablename__ = "memberships"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
        comment="FK → users.id.",
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("tenants.id"),
        nullable=False,
        comment="FK → tenants.id.",
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="staff",
        comment="Role: owner, co_owner, admin, or staff.",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        comment="Membership status: active or suspended.",
    )

    # ── Relationships ────────────────────────────────────────
    user = relationship("User", back_populates="memberships")
    tenant = relationship("Tenant", back_populates="memberships")
