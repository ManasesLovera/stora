"""
Pydantic schemas for authentication (JWT tokens).
"""

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Schema for the JWT access-token response."""

    access_token: str = Field(..., description="JWT access token.")
    token_type: str = Field(
        default="bearer", description="Token type (always 'bearer')."
    )


class TokenData(BaseModel):
    """
    Decoded token payload used internally.

    Extracted from the JWT ``sub`` claim to identify the user.
    """

    email: str | None = Field(default=None, description="User e-mail from the token.")


class LoginRequest(BaseModel):
    """Schema for the login request body."""

    email: EmailStr = Field(
        ...,
        description="Registered e-mail address.",
        examples=["alice@example.com"],
    )
    password: str = Field(
        ...,
        description="Plain-text password.",
        examples=["S3cur3P@ss!"],
    )
