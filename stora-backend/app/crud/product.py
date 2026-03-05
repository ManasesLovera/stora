"""
CRUD operations for the **Product** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def get_product(db: AsyncSession, product_id: UUID) -> Product | None:
    """Return a single product by primary key, or ``None``."""
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()


async def get_products_by_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Product]:
    """Return products for a given tenant."""
    result = await db.execute(
        select(Product)
        .where(Product.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    """Create a new product."""
    product = Product(**product_in.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(
    db: AsyncSession,
    product: Product,
    product_in: ProductUpdate,
) -> Product:
    """Update an existing product with the provided fields."""
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product: Product) -> None:
    """Delete a product from the database."""
    await db.delete(product)
    await db.commit()
