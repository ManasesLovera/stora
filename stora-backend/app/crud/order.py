"""
CRUD operations for the **Order** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


async def get_order(db: AsyncSession, order_id: UUID) -> Order | None:
    """Return a single order by primary key, or ``None``."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalars().first()


async def get_orders_by_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Order]:
    """Return orders for a given tenant."""
    result = await db.execute(
        select(Order)
        .where(Order.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_orders_by_user(
    db: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Order]:
    """Return orders placed by a given user."""
    result = await db.execute(
        select(Order)
        .where(Order.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order:
    """Create a new order."""
    order = Order(**order_in.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def update_order(
    db: AsyncSession,
    order: Order,
    order_in: OrderUpdate,
) -> Order:
    """Update an existing order with the provided fields."""
    for field, value in order_in.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order: Order) -> None:
    """Delete an order from the database."""
    await db.delete(order)
    await db.commit()
