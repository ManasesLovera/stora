"""
Tests for the Tenants CRUD endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.test_auth import get_auth_header
from tests.test_plans import PLAN_PAYLOAD, create_plan


async def create_tenant(
    client: AsyncClient,
    headers: dict,
    plan_id: str,
    slug: str = "test-shop",
):
    """Helper: create a tenant and return the response."""
    return await client.post(
        "/api/v1/tenants/",
        json={
            "name": "Test Shop",
            "slug": slug,
            "plan_id": plan_id,
            "settings": {"theme": "dark"},
        },
        headers=headers,
    )


async def setup_plan(client: AsyncClient, headers: dict) -> str:
    """Helper: create a plan and return its ID."""
    resp = await create_plan(client, headers)
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_tenant(client: AsyncClient):
    """POST /api/v1/tenants/ creates a tenant and returns 201."""
    headers = await get_auth_header(client)
    plan_id = await setup_plan(client, headers)

    response = await create_tenant(client, headers, plan_id)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Test Shop"
    assert data["slug"] == "test-shop"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio
async def test_create_tenant_duplicate_slug(client: AsyncClient):
    """Creating two tenants with the same slug returns 400."""
    headers = await get_auth_header(client)
    plan_id = await setup_plan(client, headers)

    await create_tenant(client, headers, plan_id, slug="dup-slug")
    response = await create_tenant(client, headers, plan_id, slug="dup-slug")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_tenants(client: AsyncClient):
    """GET /api/v1/tenants/ returns tenants."""
    headers = await get_auth_header(client)
    plan_id = await setup_plan(client, headers)
    await create_tenant(client, headers, plan_id)

    response = await client.get("/api/v1/tenants/", headers=headers)
    assert response.status_code == 200

    tenants = response.json()
    assert isinstance(tenants, list)
    assert len(tenants) >= 1


@pytest.mark.asyncio
async def test_get_tenant_by_id(client: AsyncClient):
    """GET /api/v1/tenants/{id} returns the correct tenant."""
    headers = await get_auth_header(client)
    plan_id = await setup_plan(client, headers)
    create_resp = await create_tenant(client, headers, plan_id)
    tenant_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/tenants/{tenant_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == tenant_id


@pytest.mark.asyncio
async def test_update_tenant(client: AsyncClient):
    """PATCH /api/v1/tenants/{id} updates the tenant."""
    headers = await get_auth_header(client)
    plan_id = await setup_plan(client, headers)
    create_resp = await create_tenant(client, headers, plan_id)
    tenant_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/tenants/{tenant_id}",
        json={"name": "Updated Shop"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Shop"


@pytest.mark.asyncio
async def test_delete_tenant(client: AsyncClient):
    """DELETE /api/v1/tenants/{id} removes the tenant."""
    headers = await get_auth_header(client)
    plan_id = await setup_plan(client, headers)
    create_resp = await create_tenant(client, headers, plan_id)
    tenant_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/tenants/{tenant_id}", headers=headers)
    assert del_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/tenants/{tenant_id}", headers=headers)
    assert get_resp.status_code == 404
