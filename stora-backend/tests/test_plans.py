"""
Tests for the Plans CRUD endpoints.
"""

import pytest
from httpx import AsyncClient

from tests.test_auth import get_auth_header

PLAN_PAYLOAD = {
    "name": "Pro",
    "price": 29.99,
    "interval": "monthly",
    "features": {"max_products": 100, "max_staff": 10, "has_ai": True},
}


async def create_plan(client: AsyncClient, headers: dict, payload: dict | None = None):
    """Helper: create a plan and return the response."""
    return await client.post(
        "/api/v1/plans/",
        json=payload or PLAN_PAYLOAD,
        headers=headers,
    )


@pytest.mark.asyncio
async def test_create_plan(client: AsyncClient):
    """POST /api/v1/plans/ creates a plan and returns 201."""
    headers = await get_auth_header(client)
    response = await create_plan(client, headers)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == PLAN_PAYLOAD["name"]
    assert data["price"] == PLAN_PAYLOAD["price"]
    assert "id" in data


@pytest.mark.asyncio
async def test_list_plans_public(client: AsyncClient):
    """GET /api/v1/plans/ is public and returns plans."""
    headers = await get_auth_header(client)
    await create_plan(client, headers)

    # List without auth
    response = await client.get("/api/v1/plans/")
    assert response.status_code == 200
    plans = response.json()
    assert isinstance(plans, list)
    assert len(plans) >= 1


@pytest.mark.asyncio
async def test_get_plan_by_id(client: AsyncClient):
    """GET /api/v1/plans/{id} returns the correct plan."""
    headers = await get_auth_header(client)
    create_resp = await create_plan(client, headers)
    plan_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/plans/{plan_id}")
    assert response.status_code == 200
    assert response.json()["id"] == plan_id


@pytest.mark.asyncio
async def test_get_plan_not_found(client: AsyncClient):
    """GET /api/v1/plans/{id} with bogus UUID returns 404."""
    response = await client.get(
        "/api/v1/plans/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_plan(client: AsyncClient):
    """PATCH /api/v1/plans/{id} updates the plan's name."""
    headers = await get_auth_header(client)
    create_resp = await create_plan(client, headers)
    plan_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/plans/{plan_id}",
        json={"name": "Enterprise"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Enterprise"


@pytest.mark.asyncio
async def test_delete_plan(client: AsyncClient):
    """DELETE /api/v1/plans/{id} removes the plan."""
    headers = await get_auth_header(client)
    create_resp = await create_plan(client, headers)
    plan_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/plans/{plan_id}", headers=headers)
    assert del_resp.status_code == 204

    # Verify gone
    get_resp = await client.get(f"/api/v1/plans/{plan_id}")
    assert get_resp.status_code == 404
