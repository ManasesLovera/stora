"""
Combo Items router – CRUD endpoints for combo (bundle) items.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.combo_item import (
    create_combo_item,
    delete_combo_item,
    get_combo_item,
    get_combo_items_by_parent,
    update_combo_item,
)
from app.database import get_db
from app.models.user import User
from app.schemas.combo_item import ComboItemCreate, ComboItemRead, ComboItemUpdate

router = APIRouter()


@router.get(
    "/product/{parent_id}",
    response_model=list[ComboItemRead],
    summary="List combo items by parent product",
    description="Return all items in a combo product.",
)
async def list_combo_items(
    parent_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[ComboItemRead]:
    """Return all combo items for a given parent (combo) product."""
    return await get_combo_items_by_parent(db, parent_id)


@router.get(
    "/{combo_item_id}",
    response_model=ComboItemRead,
    summary="Get combo item by ID",
    description="Return a single combo item.",
)
async def read_combo_item(
    combo_item_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ComboItemRead:
    """Return a combo item by primary key."""
    combo_item = await get_combo_item(db, combo_item_id)
    if not combo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combo item not found.",
        )
    return combo_item


@router.post(
    "/",
    response_model=ComboItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create combo item",
    description="Add a product to a combo.",
)
async def create_combo_item_endpoint(
    combo_item_in: ComboItemCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ComboItemRead:
    """Create a new combo item."""
    return await create_combo_item(db, combo_item_in)


@router.patch(
    "/{combo_item_id}",
    response_model=ComboItemRead,
    summary="Update combo item",
    description="Update the quantity of a combo item.",
)
async def update_combo_item_endpoint(
    combo_item_id: UUID,
    combo_item_in: ComboItemUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ComboItemRead:
    """Update combo item fields."""
    combo_item = await get_combo_item(db, combo_item_id)
    if not combo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combo item not found.",
        )
    return await update_combo_item(db, combo_item, combo_item_in)


@router.delete(
    "/{combo_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete combo item",
    description="Remove a product from a combo.",
)
async def delete_combo_item_endpoint(
    combo_item_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a combo item by primary key."""
    combo_item = await get_combo_item(db, combo_item_id)
    if not combo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combo item not found.",
        )
    await delete_combo_item(db, combo_item)
