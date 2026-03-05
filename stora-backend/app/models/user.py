"""
User model – represents a person who can authenticate, place orders,
book appointments, and belong to one or more tenants via memberships.
"""

import uuid

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """
    A registered user of the Stora platform.

    Attributes:
        id:         Unique identifier (UUID).
        email:      Unique e-mail address used for authentication.
        full_name:  Display name.
        avatar_url: Optional URL to profile picture.
        hashed_password: Bcrypt-hashed password for authentication.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique e-mail address used for login.",
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Full display name of the user.",
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="Optional URL pointing to the user's profile picture.",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Bcrypt-hashed password.",
    )

    # ── Relationships ────────────────────────────────────────
    memberships = relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    appointments = relationship(
        "Appointment",
        back_populates="user",
        foreign_keys="[Appointment.user_id]",
        cascade="all, delete-orphan",
    )
