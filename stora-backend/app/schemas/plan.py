"""
Pydantic schemas for the **Plan** entity.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PlanCreate(BaseModel):
    """Schema for creating a new subscription plan."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Plan name, e.g. Basic, Pro, Enterprise.",
        examples=["Pro"],
    )
    price: float = Field(
        ...,
        ge=0,
        description="Price per billing interval.",
        examples=[29.99],
    )
    interval: str = Field(
        default="monthly",
        description="Billing cycle: 'monthly' or 'yearly'.",
        examples=["monthly"],
    )
    features: dict = Field(
        default_factory=dict,
        description="JSON with feature flags and limits.",
        examples=[{"max_products": 100, "max_staff": 10, "has_ai": True}],
    )


class PlanUpdate(BaseModel):
    """Schema for partially updating a plan."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, ge=0)
    interval: str | None = Field(default=None)
    features: dict | None = Field(default=None)


class PlanRead(BaseModel):
    """Schema returned when reading plan data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Plan UUID.")
    name: str = Field(..., description="Plan name.")
    price: float = Field(..., description="Price per billing interval.")
    interval: str = Field(..., description="Billing cycle.")
    features: dict = Field(..., description="Feature flags and limits.")
