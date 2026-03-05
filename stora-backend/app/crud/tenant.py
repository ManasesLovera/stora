"""
CRUD operations for the **Tenant** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


async def get_tenant(db: AsyncSession, tenant_id: UUID) -> Tenant | None:
    """Return a single tenant by primary key, or ``None``."""
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
    return result.scalars().first()


async def get_tenant_by_slug(db: AsyncSession, slug: str) -> Tenant | None:
    """Return a single tenant by slug, or ``None``."""
    result = await db.execute(select(Tenant).where(Tenant.slug == slug))
    return result.scalars().first()


async def get_tenants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[Tenant]:
    """Return a paginated list of tenants."""
    result = await db.execute(select(Tenant).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_tenant(db: AsyncSession, tenant_in: TenantCreate) -> Tenant:
    """Create a new tenant."""
    tenant = Tenant(**tenant_in.model_dump())
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return tenant


async def update_tenant(
    db: AsyncSession,
    tenant: Tenant,
    tenant_in: TenantUpdate,
) -> Tenant:
    """Update an existing tenant with the provided fields."""
    for field, value in tenant_in.model_dump(exclude_unset=True).items():
        setattr(tenant, field, value)

    await db.commit()
    await db.refresh(tenant)
    return tenant


async def delete_tenant(db: AsyncSession, tenant: Tenant) -> None:
    """Delete a tenant from the database."""
    await db.delete(tenant)
    await db.commit()
