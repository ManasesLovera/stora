"""
Plan model – defines the subscription tiers available to tenants
(e.g. Basic, Pro, Enterprise) and their feature limits.
"""

import uuid

from sqlalchemy import Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Plan(Base):
    """
    A subscription plan that governs the features and limits for a tenant.

    Attributes:
        id:       Unique identifier (UUID).
        name:     Human-readable plan name (e.g. "Basic", "Pro").
        price:    Cost per billing interval.
        interval: Billing cycle – ``"monthly"`` or ``"yearly"``.
        features: JSON object with feature flags / limits
                  (e.g. ``{"max_products": 50, "max_staff": 5, "has_ai": false}``).
    """

    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Plan name, e.g. Basic, Pro, Enterprise.",
    )
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Price per billing interval.",
    )
    interval: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="monthly",
        comment="Billing cycle: 'monthly' or 'yearly'.",
    )
    features: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        comment="JSON with feature flags and limits.",
    )

    # ── Relationships ────────────────────────────────────────
    tenants = relationship(
        "Tenant",
        back_populates="plan",
    )
