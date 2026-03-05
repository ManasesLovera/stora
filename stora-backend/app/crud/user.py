"""
CRUD operations for the **User** model.

Every function receives an ``AsyncSession`` and returns either model
instances or ``None``.  The session is **not** committed here – the
caller (router) is responsible for committing after a successful
operation.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: UUID) -> User | None:
    """Return a single user by primary key, or ``None``."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Return a single user by e-mail address, or ``None``."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """Return a paginated list of users."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    Create a new user.

    The plain-text password is hashed before storage.
    """
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        avatar_url=user_in.avatar_url,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession,
    user: User,
    user_in: UserUpdate,
) -> User:
    """
    Update an existing user with the provided fields.

    Only fields that are explicitly set (not ``None``) are updated.
    """
    update_data = user_in.model_dump(exclude_unset=True)

    # Hash the new password if provided
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    """Delete a user from the database."""
    await db.delete(user)
    await db.commit()
