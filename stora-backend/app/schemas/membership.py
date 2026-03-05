"""
Pydantic schemas for the **Membership** entity.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MembershipCreate(BaseModel):
    """Schema for creating a membership (linking a user to a tenant)."""

    user_id: UUID = Field(..., description="UUID of the user.")
    tenant_id: UUID = Field(..., description="UUID of the tenant.")
    role: str = Field(
        default="staff",
        description="Role: owner, co_owner, admin, or staff.",
        examples=["admin"],
    )
    status: str = Field(
        default="active",
        description="Membership status: active or suspended.",
    )


class MembershipUpdate(BaseModel):
    """Schema for updating a membership."""

    role: str | None = Field(default=None, description="New role.")
    status: str | None = Field(default=None, description="New status.")


class MembershipRead(BaseModel):
    """Schema returned when reading membership data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Membership UUID.")
    user_id: UUID = Field(..., description="FK to user.")
    tenant_id: UUID = Field(..., description="FK to tenant.")
    role: str = Field(..., description="Role within the tenant.")
    status: str = Field(..., description="Membership status.")
