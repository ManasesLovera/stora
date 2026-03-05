"""
Tests for the Invitations CRUD endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.test_auth import get_auth_header
from tests.test_plans import create_plan
from tests.test_tenants import create_tenant


async def setup_tenant(client: AsyncClient, headers: dict) -> str:
    """Helper: create a plan + tenant and return the tenant ID."""
    plan_resp = await create_plan(client, headers)
    plan_id = plan_resp.json()["id"]
    tenant_resp = await create_tenant(client, headers, plan_id)
    return tenant_resp.json()["id"]


@pytest.mark.asyncio
async def test_create_invitation(client: AsyncClient):
    """POST /api/v1/invitations/ creates an invitation."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    response = await client.post(
        "/api/v1/invitations/",
        json={
            "tenant_id": tenant_id,
            "email": "invitee@example.com",
            "role": "admin",
        },
        headers=headers,
    )
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "invitee@example.com"
    assert data["role"] == "admin"
    assert "token" in data
    assert "expires_at" in data


@pytest.mark.asyncio
async def test_list_invitations_by_tenant(client: AsyncClient):
    """GET /api/v1/invitations/tenant/{id} returns invitations."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    await client.post(
        "/api/v1/invitations/",
        json={
            "tenant_id": tenant_id,
            "email": "staff@example.com",
            "role": "staff",
        },
        headers=headers,
    )

    response = await client.get(
        f"/api/v1/invitations/tenant/{tenant_id}", headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_invitation_by_token(client: AsyncClient):
    """GET /api/v1/invitations/token/{token} returns the invitation (public)."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    create_resp = await client.post(
        "/api/v1/invitations/",
        json={
            "tenant_id": tenant_id,
            "email": "token-test@example.com",
            "role": "staff",
        },
        headers=headers,
    )
    token = create_resp.json()["token"]

    # Public endpoint — no auth header
    response = await client.get(f"/api/v1/invitations/token/{token}")
    assert response.status_code == 200
    assert response.json()["token"] == token


@pytest.mark.asyncio
async def test_delete_invitation(client: AsyncClient):
    """DELETE /api/v1/invitations/{id} removes the invitation."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    create_resp = await client.post(
        "/api/v1/invitations/",
        json={
            "tenant_id": tenant_id,
            "email": "delete-me@example.com",
            "role": "staff",
        },
        headers=headers,
    )
    invitation_id = create_resp.json()["id"]

    del_resp = await client.delete(
        f"/api/v1/invitations/{invitation_id}", headers=headers
    )
    assert del_resp.status_code == 204
