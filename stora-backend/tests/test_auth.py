"""
Tests for the authentication endpoints (register and login).
"""

import pytest
from httpx import AsyncClient

# ── Test data ────────────────────────────────────────────────
REGISTER_PAYLOAD = {
    "email": "testuser@example.com",
    "full_name": "Test User",
    "password": "SecurePass123!",
}


# ── Helper ───────────────────────────────────────────────────
async def register_user(client: AsyncClient, payload: dict | None = None):
    """Register a user and return the response."""
    return await client.post(
        "/api/v1/auth/register",
        json=payload or REGISTER_PAYLOAD,
    )


async def login_user(client: AsyncClient, email: str, password: str):
    """Log in a user and return the response."""
    return await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


async def get_auth_header(client: AsyncClient) -> dict:
    """Register + login and return the Authorization header dict."""
    await register_user(client)
    resp = await login_user(client, REGISTER_PAYLOAD["email"], REGISTER_PAYLOAD["password"])
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Registration tests ───────────────────────────────────────
@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Registering a new user returns 201 with user data."""
    response = await register_user(client)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == REGISTER_PAYLOAD["email"]
    assert data["full_name"] == REGISTER_PAYLOAD["full_name"]
    assert "id" in data
    # Password must never be returned
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Registering with an existing e-mail returns 400."""
    await register_user(client)
    response = await register_user(client)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    """Registering with an invalid e-mail returns 422."""
    payload = {**REGISTER_PAYLOAD, "email": "not-an-email"}
    response = await register_user(client, payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    """Registering with a too-short password returns 422."""
    payload = {**REGISTER_PAYLOAD, "password": "short"}
    response = await register_user(client, payload)
    assert response.status_code == 422


# ── Login tests ──────────────────────────────────────────────
@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Logging in with valid credentials returns a JWT token."""
    await register_user(client)
    response = await login_user(
        client,
        REGISTER_PAYLOAD["email"],
        REGISTER_PAYLOAD["password"],
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Logging in with wrong password returns 401."""
    await register_user(client)
    response = await login_user(client, REGISTER_PAYLOAD["email"], "WrongPassword!")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Logging in with a non-existent e-mail returns 401."""
    response = await login_user(client, "nobody@example.com", "whatever")
    assert response.status_code == 401


# ── Protected endpoint access ────────────────────────────────
@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    """Accessing a protected endpoint without a token returns 401."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token(client: AsyncClient):
    """Accessing a protected endpoint with an invalid token returns 401."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    """GET /api/v1/users/me returns the authenticated user's profile."""
    headers = await get_auth_header(client)
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == REGISTER_PAYLOAD["email"]
    assert data["full_name"] == REGISTER_PAYLOAD["full_name"]
