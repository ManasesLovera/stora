"""
Tests for the Products CRUD endpoints.
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


PRODUCT_PAYLOAD = {
    "name": "Cappuccino",
    "price": 4.50,
    "is_combo": False,
    "stock": 100,
}


async def create_product(
    client: AsyncClient,
    headers: dict,
    tenant_id: str,
    payload: dict | None = None,
):
    """Helper: create a product and return the response."""
    data = {**(payload or PRODUCT_PAYLOAD), "tenant_id": tenant_id}
    return await client.post("/api/v1/products/", json=data, headers=headers)


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    """POST /api/v1/products/ creates a product and returns 201."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    response = await create_product(client, headers, tenant_id)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Cappuccino"
    assert data["price"] == 4.5
    assert data["stock"] == 100


@pytest.mark.asyncio
async def test_list_products_by_tenant(client: AsyncClient):
    """GET /api/v1/products/tenant/{id} returns products."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    await create_product(client, headers, tenant_id)

    response = await client.get(
        f"/api/v1/products/tenant/{tenant_id}", headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient):
    """GET /api/v1/products/{id} returns the correct product."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/products/{product_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == product_id


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    """PATCH /api/v1/products/{id} updates the product."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/products/{product_id}",
        json={"name": "Latte", "price": 5.0},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Latte"
    assert response.json()["price"] == 5.0


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    """DELETE /api/v1/products/{id} removes the product."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    del_resp = await client.delete(
        f"/api/v1/products/{product_id}", headers=headers
    )
    assert del_resp.status_code == 204

    get_resp = await client.get(
        f"/api/v1/products/{product_id}", headers=headers
    )
    assert get_resp.status_code == 404
