"""
Tenant model – represents a business (store / organisation) on the
Stora platform.  Each tenant has its own products, orders, members,
and settings.
"""

import uuid

from sqlalchemy import JSON, Boolean, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Tenant(Base):
    """
    A business account (tenant) in the multi-tenant SaaS platform.

    Attributes:
        id:        Unique identifier (UUID).
        name:      Business display name.
        slug:      URL-safe unique identifier for the tenant.
        plan_id:   Foreign key to the subscription plan.
        settings:  JSON object for themes, logos, active features, etc.
        is_active: Whether the tenant account is currently active.
    """

    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Business display name.",
    )
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="URL-safe unique slug for the tenant.",
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("plans.id"),
        nullable=False,
        comment="FK → plans.id – subscription plan for this tenant.",
    )
    settings: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
        comment="JSON with theme, logos, active_features, etc.",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether this tenant account is active.",
    )

    # ── Relationships ────────────────────────────────────────
    plan = relationship("Plan", back_populates="tenants")
    memberships = relationship(
        "Membership",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    invitations = relationship(
        "Invitation",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    products = relationship(
        "Product",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    orders = relationship(
        "Order",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    appointments = relationship(
        "Appointment",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
