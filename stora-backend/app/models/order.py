"""
Order model – represents a purchase made by a user within a tenant's
store.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Order(Base):
    """
    A customer order recorded by a tenant.

    Attributes:
        id:         Unique identifier (UUID).
        tenant_id:  FK → tenants.id – tenant that owns the order.
        user_id:    FK → users.id – the customer.
        total:      Total price of the order.
        status:     Current order status (e.g. 'pending', 'completed').
        created_at: Timestamp when the order was placed.
    """

    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("tenants.id"),
        nullable=False,
        comment="FK → tenants.id – owning tenant.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
        comment="FK → users.id – the customer who placed the order.",
    )
    total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Total amount for the order.",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        comment="Order status, e.g. pending, confirmed, completed, cancelled.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp when the order was created.",
    )

    # ── Relationships ────────────────────────────────────────
    tenant = relationship("Tenant", back_populates="orders")
    user = relationship("User", back_populates="orders")
