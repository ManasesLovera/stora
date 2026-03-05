"""
Pydantic schemas for the **Product** entity.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Schema for creating a new product."""

    tenant_id: UUID = Field(..., description="UUID of the owning tenant.")
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Product display name.",
        examples=["Cappuccino"],
    )
    price: float = Field(
        ...,
        ge=0,
        description="Unit price.",
        examples=[4.50],
    )
    is_combo: bool = Field(
        default=False,
        description="True if this product is a combo/bundle.",
    )
    stock: int = Field(
        default=0,
        ge=0,
        description="Available inventory count.",
        examples=[100],
    )


class ProductUpdate(BaseModel):
    """Schema for partially updating a product."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    price: float | None = Field(default=None, ge=0)
    is_combo: bool | None = Field(default=None)
    stock: int | None = Field(default=None, ge=0)


class ProductRead(BaseModel):
    """Schema returned when reading product data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Product UUID.")
    tenant_id: UUID = Field(..., description="FK to owning tenant.")
    name: str = Field(..., description="Product name.")
    price: float = Field(..., description="Unit price.")
    is_combo: bool = Field(..., description="Combo flag.")
    stock: int = Field(..., description="Stock count.")
