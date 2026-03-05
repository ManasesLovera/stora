"""
CRUD operations for the **ComboItem** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.combo_item import ComboItem
from app.schemas.combo_item import ComboItemCreate, ComboItemUpdate


async def get_combo_item(db: AsyncSession, combo_item_id: UUID) -> ComboItem | None:
    """Return a single combo item by primary key, or ``None``."""
    result = await db.execute(
        select(ComboItem).where(ComboItem.id == combo_item_id)
    )
    return result.scalars().first()


async def get_combo_items_by_parent(
    db: AsyncSession,
    parent_id: UUID,
) -> list[ComboItem]:
    """Return all combo items for a given parent (combo) product."""
    result = await db.execute(
        select(ComboItem).where(ComboItem.parent_id == parent_id)
    )
    return list(result.scalars().all())


async def create_combo_item(
    db: AsyncSession,
    combo_item_in: ComboItemCreate,
) -> ComboItem:
    """Create a new combo item."""
    combo_item = ComboItem(**combo_item_in.model_dump())
    db.add(combo_item)
    await db.commit()
    await db.refresh(combo_item)
    return combo_item


async def update_combo_item(
    db: AsyncSession,
    combo_item: ComboItem,
    combo_item_in: ComboItemUpdate,
) -> ComboItem:
    """Update an existing combo item with the provided fields."""
    for field, value in combo_item_in.model_dump(exclude_unset=True).items():
        setattr(combo_item, field, value)

    await db.commit()
    await db.refresh(combo_item)
    return combo_item


async def delete_combo_item(db: AsyncSession, combo_item: ComboItem) -> None:
    """Delete a combo item from the database."""
    await db.delete(combo_item)
    await db.commit()
