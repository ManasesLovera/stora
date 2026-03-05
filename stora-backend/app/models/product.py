"""
Product model – items or services that a tenant sells.
A product may be a simple item or a **combo** (bundle of other products).
"""

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    """
    A product or service offered by a tenant.

    Attributes:
        id:        Unique identifier (UUID).
        tenant_id: FK → tenants.id – the owning tenant.
        name:      Product display name.
        price:     Unit price.
        is_combo:  Whether this product is a bundle of other products.
        stock:     Available inventory count.
    """

    __tablename__ = "products"

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
        comment="FK → tenants.id – owning tenant.",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Product display name.",
    )
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Unit price of the product.",
    )
    is_combo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True if this product is a combo (bundle).",
    )
    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Available inventory count.",
    )

    # ── Relationships ────────────────────────────────────────
    tenant = relationship("Tenant", back_populates="products")
    combo_items = relationship(
        "ComboItem",
        back_populates="parent",
        foreign_keys="[ComboItem.parent_id]",
        cascade="all, delete-orphan",
    )
