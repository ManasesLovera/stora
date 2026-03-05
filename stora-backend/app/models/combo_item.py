"""
ComboItem model – represents a child product inside a combo (bundle).
Each row links a *parent* combo product to a *child* product with a
quantity.
"""

import uuid

from sqlalchemy import ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ComboItem(Base):
    """
    A single item within a combo product.

    Attributes:
        id:        Unique identifier (UUID).
        parent_id: FK → products.id – the combo product.
        child_id:  FK → products.id – the contained product.
        quantity:  How many units of the child product are in the combo.
    """

    __tablename__ = "combo_items"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key – auto-generated UUID.",
    )
    parent_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("products.id"),
        nullable=False,
        comment="FK → products.id – the combo product.",
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("products.id"),
        nullable=False,
        comment="FK → products.id – the contained product.",
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="Number of child product units in the combo.",
    )

    # ── Relationships ────────────────────────────────────────
    parent = relationship(
        "Product",
        back_populates="combo_items",
        foreign_keys=[parent_id],
    )
    child = relationship(
        "Product",
        foreign_keys=[child_id],
    )
