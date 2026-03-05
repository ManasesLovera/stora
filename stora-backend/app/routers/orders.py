"""
Orders router – CRUD endpoints for customer orders.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.order import (
    create_order,
    delete_order,
    get_order,
    get_orders_by_tenant,
    update_order,
)
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate

router = APIRouter()


@router.get(
    "/tenant/{tenant_id}",
    response_model=list[OrderRead],
    summary="List orders by tenant",
    description="Return orders for a specific tenant.",
)
async def list_orders(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[OrderRead]:
    """Return all orders for a given tenant."""
    return await get_orders_by_tenant(db, tenant_id, skip=skip, limit=limit)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    summary="Get order by ID",
    description="Return a single order.",
)
async def read_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    """Return an order by primary key."""
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    return order


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create order",
    description="Place a new order.",
)
async def create_order_endpoint(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    """Create a new order."""
    return await create_order(db, order_in)


@router.patch(
    "/{order_id}",
    response_model=OrderRead,
    summary="Update order",
    description="Partially update an order (e.g. change status).",
)
async def update_order_endpoint(
    order_id: UUID,
    order_in: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    """Update order fields."""
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    return await update_order(db, order, order_in)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete order",
    description="Permanently delete an order.",
)
async def delete_order_endpoint(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete an order by primary key."""
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    await delete_order(db, order)
