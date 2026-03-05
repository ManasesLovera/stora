"""
Pydantic schemas for the **User** entity.

Three schemas cover the typical CRUD lifecycle:
- ``UserCreate``  – payload for registering a new user.
- ``UserUpdate``  – payload for updating an existing user (all fields optional).
- ``UserRead``    – response model returned to the client.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user (registration)."""

    email: EmailStr = Field(
        ...,
        description="Unique e-mail address for the new user.",
        examples=["alice@example.com"],
    )
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Full display name.",
        examples=["Alice Johnson"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plain-text password (will be hashed server-side).",
        examples=["S3cur3P@ss!"],
    )
    avatar_url: str | None = Field(
        default=None,
        max_length=512,
        description="Optional URL to profile picture.",
    )


class UserUpdate(BaseModel):
    """Schema for partially updating a user profile."""

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New display name.",
    )
    avatar_url: str | None = Field(
        default=None,
        max_length=512,
        description="New avatar URL.",
    )
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="New plain-text password.",
    )


class UserRead(BaseModel):
    """Schema returned when reading user data – never exposes the password."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="User UUID.")
    email: EmailStr = Field(..., description="User e-mail.")
    full_name: str = Field(..., description="Display name.")
    avatar_url: str | None = Field(None, description="Profile picture URL.")
