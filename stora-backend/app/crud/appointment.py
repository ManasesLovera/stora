"""
CRUD operations for the **Appointment** model.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


async def get_appointment(
    db: AsyncSession,
    appointment_id: UUID,
) -> Appointment | None:
    """Return a single appointment by primary key, or ``None``."""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    return result.scalars().first()


async def get_appointments_by_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Appointment]:
    """Return appointments for a given tenant."""
    result = await db.execute(
        select(Appointment)
        .where(Appointment.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_appointments_by_user(
    db: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Appointment]:
    """Return appointments booked by a given user."""
    result = await db.execute(
        select(Appointment)
        .where(Appointment.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_appointment(
    db: AsyncSession,
    appointment_in: AppointmentCreate,
) -> Appointment:
    """Create a new appointment."""
    appointment = Appointment(**appointment_in.model_dump())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def update_appointment(
    db: AsyncSession,
    appointment: Appointment,
    appointment_in: AppointmentUpdate,
) -> Appointment:
    """Update an existing appointment with the provided fields."""
    for field, value in appointment_in.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)

    await db.commit()
    await db.refresh(appointment)
    return appointment


async def delete_appointment(
    db: AsyncSession,
    appointment: Appointment,
) -> None:
    """Delete an appointment from the database."""
    await db.delete(appointment)
    await db.commit()
