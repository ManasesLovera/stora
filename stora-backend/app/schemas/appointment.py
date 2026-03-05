"""
Pydantic schemas for the **Appointment** entity.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    """Schema for booking a new appointment."""

    tenant_id: UUID = Field(..., description="UUID of the tenant.")
    user_id: UUID = Field(..., description="UUID of the customer.")
    staff_id: UUID = Field(..., description="UUID of the assigned staff membership.")
    scheduled_at: datetime = Field(
        ...,
        description="Date and time of the appointment.",
    )
    status: str = Field(
        default="scheduled",
        description="Appointment status: scheduled, completed, cancelled.",
    )


class AppointmentUpdate(BaseModel):
    """Schema for partially updating an appointment."""

    staff_id: UUID | None = Field(default=None)
    scheduled_at: datetime | None = Field(default=None)
    status: str | None = Field(default=None)


class AppointmentRead(BaseModel):
    """Schema returned when reading appointment data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Appointment UUID.")
    tenant_id: UUID = Field(..., description="FK to tenant.")
    user_id: UUID = Field(..., description="FK to customer.")
    staff_id: UUID = Field(..., description="FK to staff membership.")
    scheduled_at: datetime = Field(..., description="Scheduled date/time.")
    status: str = Field(..., description="Appointment status.")
