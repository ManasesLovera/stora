"""
Pydantic schemas for the **Order** entity.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    """Schema for creating a new order."""

    tenant_id: UUID = Field(..., description="UUID of the tenant.")
    user_id: UUID = Field(..., description="UUID of the customer.")
    total: float = Field(
        ...,
        ge=0,
        description="Total price of the order.",
        examples=[59.99],
    )
    status: str = Field(
        default="pending",
        description="Order status, e.g. pending, confirmed, completed, cancelled.",
    )


class OrderUpdate(BaseModel):
    """Schema for partially updating an order."""

    total: float | None = Field(default=None, ge=0)
    status: str | None = Field(default=None)


class OrderRead(BaseModel):
    """Schema returned when reading order data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Order UUID.")
    tenant_id: UUID = Field(..., description="FK to tenant.")
    user_id: UUID = Field(..., description="FK to customer.")
    total: float = Field(..., description="Total amount.")
    status: str = Field(..., description="Order status.")
    created_at: datetime = Field(..., description="Creation timestamp.")
