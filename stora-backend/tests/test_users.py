"""
Tests for the Users CRUD endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.test_auth import REGISTER_PAYLOAD, get_auth_header


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    """GET /api/v1/users/ returns a list including the registered user."""
    headers = await get_auth_header(client)
    response = await client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1
    assert users[0]["email"] == REGISTER_PAYLOAD["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient):
    """GET /api/v1/users/{id} returns the correct user."""
    headers = await get_auth_header(client)

    # Get current user to find the ID
    me_resp = await client.get("/api/v1/users/me", headers=headers)
    user_id = me_resp.json()["id"]

    response = await client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    """GET /api/v1/users/{id} with bogus UUID returns 404."""
    headers = await get_auth_header(client)
    response = await client.get(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    """PATCH /api/v1/users/{id} updates the user's name."""
    headers = await get_auth_header(client)

    me_resp = await client.get("/api/v1/users/me", headers=headers)
    user_id = me_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/users/{user_id}",
        json={"full_name": "Updated Name"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    """DELETE /api/v1/users/{id} removes the user."""
    # Register a second user to delete
    second_user = {
        "email": "todelete@example.com",
        "full_name": "Delete Me",
        "password": "SecurePass123!",
    }
    reg_resp = await client.post("/api/v1/auth/register", json=second_user)
    user_id = reg_resp.json()["id"]

    headers = await get_auth_header(client)

    del_resp = await client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert del_resp.status_code == 204

    # Verify the user is gone
    get_resp = await client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert get_resp.status_code == 404
