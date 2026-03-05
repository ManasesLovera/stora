"""
Users router – CRUD endpoints for user management.

All endpoints (except registration, handled in auth) require a valid
JWT bearer token.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.crud.user import delete_user, get_user, get_users, update_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter()


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user profile",
    description="Return the profile of the currently authenticated user.",
)
async def read_current_user(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Return the authenticated user's profile."""
    return current_user


@router.get(
    "/",
    response_model=list[UserRead],
    summary="List users",
    description="Return a paginated list of users. Requires authentication.",
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[UserRead]:
    """Return a paginated list of all users."""
    return await get_users(db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get user by ID",
    description="Return a single user's profile by their UUID.",
)
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> UserRead:
    """Return a user by primary key."""
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Update user",
    description="Partially update a user's profile.",
)
async def update_user_endpoint(
    user_id: UUID,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> UserRead:
    """Update user fields. Only provided fields are changed."""
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return await update_user(db, user, user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Permanently delete a user account.",
)
async def delete_user_endpoint(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a user by primary key."""
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    await delete_user(db, user)
