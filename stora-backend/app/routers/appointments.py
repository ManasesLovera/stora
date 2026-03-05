"""
Appointments router – CRUD endpoints for scheduled appointments.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.appointment import (
    create_appointment,
    delete_appointment,
    get_appointment,
    get_appointments_by_tenant,
    update_appointment,
)
from app.database import get_db
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate

router = APIRouter()


@router.get(
    "/tenant/{tenant_id}",
    response_model=list[AppointmentRead],
    summary="List appointments by tenant",
    description="Return appointments for a specific tenant.",
)
async def list_appointments(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[AppointmentRead]:
    """Return all appointments for a given tenant."""
    return await get_appointments_by_tenant(db, tenant_id, skip=skip, limit=limit)


@router.get(
    "/{appointment_id}",
    response_model=AppointmentRead,
    summary="Get appointment by ID",
    description="Return a single appointment.",
)
async def read_appointment(
    appointment_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    """Return an appointment by primary key."""
    appointment = await get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )
    return appointment


@router.post(
    "/",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create appointment",
    description="Book a new appointment.",
)
async def create_appointment_endpoint(
    appointment_in: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    """Create a new appointment."""
    return await create_appointment(db, appointment_in)


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentRead,
    summary="Update appointment",
    description="Partially update an appointment.",
)
async def update_appointment_endpoint(
    appointment_id: UUID,
    appointment_in: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    """Update appointment fields."""
    appointment = await get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )
    return await update_appointment(db, appointment, appointment_in)


@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete appointment",
    description="Cancel/delete an appointment.",
)
async def delete_appointment_endpoint(
    appointment_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete an appointment by primary key."""
    appointment = await get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )
    await delete_appointment(db, appointment)
