"""
Authentication router – login and registration endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import create_access_token, verify_password
from app.crud.user import create_user, get_user_by_email
from app.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account. The password is hashed before storage.",
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Register a new user.

    - Validates that the e-mail is not already taken.
    - Hashes the password and stores the user.
    - Returns the created user (without the password).
    """
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this e-mail already exists.",
        )
    user = await create_user(db, user_in)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Log in and receive a JWT token",
    description="Authenticate with e-mail and password to receive a bearer token.",
)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Authenticate a user and return a JWT access token.

    - Looks up the user by e-mail.
    - Verifies the password.
    - Returns a signed JWT.
    """
    user = await get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid e-mail or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)
