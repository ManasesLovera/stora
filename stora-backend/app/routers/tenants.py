"""
Tenants router – CRUD endpoints for business accounts.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.tenant import (
    create_tenant,
    delete_tenant,
    get_tenant,
    get_tenant_by_slug,
    get_tenants,
    update_tenant,
)
from app.database import get_db
from app.models.user import User
from app.schemas.tenant import TenantCreate, TenantRead, TenantUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=list[TenantRead],
    summary="List tenants",
    description="Return a paginated list of tenants.",
)
async def list_tenants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[TenantRead]:
    """Return all tenants (requires authentication)."""
    return await get_tenants(db, skip=skip, limit=limit)


@router.get(
    "/{tenant_id}",
    response_model=TenantRead,
    summary="Get tenant by ID",
    description="Return a single tenant by UUID.",
)
async def read_tenant(
    tenant_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> TenantRead:
    """Return a tenant by primary key."""
    tenant = await get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )
    return tenant


@router.post(
    "/",
    response_model=TenantRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create tenant",
    description="Create a new tenant (business account).",
)
async def create_tenant_endpoint(
    tenant_in: TenantCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> TenantRead:
    """
    Create a new tenant.

    Validates that the slug is not already in use.
    """
    existing = await get_tenant_by_slug(db, tenant_in.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A tenant with this slug already exists.",
        )
    return await create_tenant(db, tenant_in)


@router.patch(
    "/{tenant_id}",
    response_model=TenantRead,
    summary="Update tenant",
    description="Partially update a tenant's details.",
)
async def update_tenant_endpoint(
    tenant_id: UUID,
    tenant_in: TenantUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> TenantRead:
    """Update tenant fields. Only provided fields are changed."""
    tenant = await get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )
    return await update_tenant(db, tenant, tenant_in)


@router.delete(
    "/{tenant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete tenant",
    description="Permanently delete a tenant.",
)
async def delete_tenant_endpoint(
    tenant_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a tenant by primary key."""
    tenant = await get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )
    await delete_tenant(db, tenant)
