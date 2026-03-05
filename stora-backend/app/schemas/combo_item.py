"""
Pydantic schemas for the **ComboItem** entity.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ComboItemCreate(BaseModel):
    """Schema for adding a product to a combo."""

    parent_id: UUID = Field(..., description="UUID of the combo product.")
    child_id: UUID = Field(..., description="UUID of the contained product.")
    quantity: int = Field(
        default=1,
        ge=1,
        description="Number of units of the child product.",
        examples=[2],
    )


class ComboItemUpdate(BaseModel):
    """Schema for updating a combo item."""

    quantity: int | None = Field(default=None, ge=1)


class ComboItemRead(BaseModel):
    """Schema returned when reading combo item data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="ComboItem UUID.")
    parent_id: UUID = Field(..., description="FK to combo product.")
    child_id: UUID = Field(..., description="FK to contained product.")
    quantity: int = Field(..., description="Quantity in the combo.")
