"""
Appointment model – represents a scheduled service between a customer
and a staff member within a tenant.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Appointment(Base):
    """
    A booked appointment for a tenant's service.

    Attributes:
        id:           Unique identifier (UUID).
        tenant_id:    FK → tenants.id – the tenant offering the service.
        user_id:      FK → users.id – the customer booking the appointment.
        staff_id:     FK → memberships.id – the assigned staff member.
        scheduled_at: Date-time of the appointment.
        status:       Current status (e.g. 'scheduled', 'completed', 'cancelled').
    """

    __tablename__ = "appointments"

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
        comment="FK → tenants.id – tenant offering the service.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
        comment="FK → users.id – the customer.",
    )
    staff_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("memberships.id"),
        nullable=False,
        comment="FK → memberships.id – assigned staff member.",
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Date and time of the appointment.",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="scheduled",
        comment="Appointment status: scheduled, completed, cancelled.",
    )

    # ── Relationships ────────────────────────────────────────
    tenant = relationship("Tenant", back_populates="appointments")
    user = relationship(
        "User",
        back_populates="appointments",
        foreign_keys=[user_id],
    )
    staff = relationship("Membership", foreign_keys=[staff_id])
