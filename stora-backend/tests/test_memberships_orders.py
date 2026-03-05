"""
Tests for the Memberships and Orders CRUD endpoints.
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


async def get_user_id(client: AsyncClient, headers: dict) -> str:
    """Helper: return the current user's ID."""
    resp = await client.get("/api/v1/users/me", headers=headers)
    return resp.json()["id"]


# ── Membership tests ─────────────────────────────────────────
@pytest.mark.asyncio
async def test_create_membership(client: AsyncClient):
    """POST /api/v1/memberships/ creates a membership."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    response = await client.post(
        "/api/v1/memberships/",
        json={
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": "owner",
            "status": "active",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "owner"
    assert data["user_id"] == user_id
    assert data["tenant_id"] == tenant_id


@pytest.mark.asyncio
async def test_list_memberships_by_tenant(client: AsyncClient):
    """GET /api/v1/memberships/tenant/{id} returns memberships."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    await client.post(
        "/api/v1/memberships/",
        json={
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": "admin",
        },
        headers=headers,
    )

    response = await client.get(
        f"/api/v1/memberships/tenant/{tenant_id}", headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_update_membership(client: AsyncClient):
    """PATCH /api/v1/memberships/{id} updates the membership role."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    create_resp = await client.post(
        "/api/v1/memberships/",
        json={
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": "staff",
        },
        headers=headers,
    )
    membership_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/memberships/{membership_id}",
        json={"role": "admin"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


@pytest.mark.asyncio
async def test_delete_membership(client: AsyncClient):
    """DELETE /api/v1/memberships/{id} removes the membership."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    create_resp = await client.post(
        "/api/v1/memberships/",
        json={
            "user_id": user_id,
            "tenant_id": tenant_id,
            "role": "staff",
        },
        headers=headers,
    )
    membership_id = create_resp.json()["id"]

    del_resp = await client.delete(
        f"/api/v1/memberships/{membership_id}", headers=headers
    )
    assert del_resp.status_code == 204


# ── Order tests ──────────────────────────────────────────────
@pytest.mark.asyncio
async def test_create_order(client: AsyncClient):
    """POST /api/v1/orders/ creates an order."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    response = await client.post(
        "/api/v1/orders/",
        json={
            "tenant_id": tenant_id,
            "user_id": user_id,
            "total": 59.99,
            "status": "pending",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total"] == 59.99
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_orders_by_tenant(client: AsyncClient):
    """GET /api/v1/orders/tenant/{id} returns orders."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    await client.post(
        "/api/v1/orders/",
        json={
            "tenant_id": tenant_id,
            "user_id": user_id,
            "total": 10.00,
        },
        headers=headers,
    )

    response = await client.get(f"/api/v1/orders/tenant/{tenant_id}", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_update_order_status(client: AsyncClient):
    """PATCH /api/v1/orders/{id} updates the order status."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    create_resp = await client.post(
        "/api/v1/orders/",
        json={
            "tenant_id": tenant_id,
            "user_id": user_id,
            "total": 20.00,
        },
        headers=headers,
    )
    order_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/orders/{order_id}",
        json={"status": "completed"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_order(client: AsyncClient):
    """DELETE /api/v1/orders/{id} removes the order."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    user_id = await get_user_id(client, headers)

    create_resp = await client.post(
        "/api/v1/orders/",
        json={
            "tenant_id": tenant_id,
            "user_id": user_id,
            "total": 15.00,
        },
        headers=headers,
    )
    order_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/orders/{order_id}", headers=headers)
    assert del_resp.status_code == 204
