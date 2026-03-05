"""
Pydantic schemas for the **Invitation** entity.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InvitationCreate(BaseModel):
    """Schema for creating a new invitation."""

    tenant_id: UUID = Field(..., description="UUID of the tenant sending the invite.")
    email: EmailStr = Field(
        ...,
        description="E-mail address of the invitee.",
        examples=["bob@example.com"],
    )
    role: str = Field(
        default="staff",
        description="Role to assign upon acceptance.",
        examples=["admin"],
    )


class InvitationRead(BaseModel):
    """Schema returned when reading invitation data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Invitation UUID.")
    tenant_id: UUID = Field(..., description="Tenant that sent the invitation.")
    email: str = Field(..., description="Invitee e-mail.")
    role: str = Field(..., description="Role to assign.")
    token: str = Field(..., description="Unique invitation token.")
    expires_at: datetime = Field(..., description="Expiry timestamp.")
