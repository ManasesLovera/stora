"""
Products router – CRUD endpoints for products.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products_by_tenant,
    update_product,
)
from app.database import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()


@router.get(
    "/tenant/{tenant_id}",
    response_model=list[ProductRead],
    summary="List products by tenant",
    description="Return products for a specific tenant.",
)
async def list_products(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[ProductRead]:
    """Return all products for a given tenant."""
    return await get_products_by_tenant(db, tenant_id, skip=skip, limit=limit)


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Get product by ID",
    description="Return a single product.",
)
async def read_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ProductRead:
    """Return a product by primary key."""
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return product


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Add a new product to a tenant's catalog.",
)
async def create_product_endpoint(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ProductRead:
    """Create a new product."""
    return await create_product(db, product_in)


@router.patch(
    "/{product_id}",
    response_model=ProductRead,
    summary="Update product",
    description="Partially update a product.",
)
async def update_product_endpoint(
    product_id: UUID,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ProductRead:
    """Update product fields."""
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return await update_product(db, product, product_in)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Permanently delete a product.",
)
async def delete_product_endpoint(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a product by primary key."""
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    await delete_product(db, product)
