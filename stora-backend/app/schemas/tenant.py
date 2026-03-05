"""
Pydantic schemas for the **Tenant** entity.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TenantCreate(BaseModel):
    """Schema for creating a new tenant (business account)."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Business display name.",
        examples=["My Awesome Shop"],
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="URL-safe unique identifier.",
        examples=["my-awesome-shop"],
    )
    plan_id: UUID = Field(
        ...,
        description="UUID of the subscription plan.",
    )
    settings: dict = Field(
        default_factory=dict,
        description="JSON with theme, logos, active_features, etc.",
    )
    is_active: bool = Field(
        default=True,
        description="Whether the tenant is active.",
    )


class TenantUpdate(BaseModel):
    """Schema for partially updating a tenant."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    plan_id: UUID | None = Field(default=None)
    settings: dict | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class TenantRead(BaseModel):
    """Schema returned when reading tenant data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Tenant UUID.")
    name: str = Field(..., description="Business name.")
    slug: str = Field(..., description="URL-safe slug.")
    plan_id: UUID = Field(..., description="FK to subscription plan.")
    settings: dict = Field(..., description="Tenant settings.")
    is_active: bool = Field(..., description="Active flag.")
