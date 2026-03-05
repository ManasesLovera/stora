"""
Tests for the Products CRUD endpoints, including image upload.
"""

import io

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
    assert data["image_url"] is None


@pytest.mark.asyncio
async def test_create_product_with_image_url(client: AsyncClient):
    """POST /api/v1/products/ can include image_url at creation."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    payload = {
        **PRODUCT_PAYLOAD,
        "image_url": "data:image/png;base64,iVBORw0KGgo=",
    }
    response = await create_product(client, headers, tenant_id, payload=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["image_url"] == "data:image/png;base64,iVBORw0KGgo="


@pytest.mark.asyncio
async def test_list_products_by_tenant(client: AsyncClient):
    """GET /api/v1/products/tenant/{id} returns products."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    await create_product(client, headers, tenant_id)

    response = await client.get(f"/api/v1/products/tenant/{tenant_id}", headers=headers)
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
async def test_update_product_image_url(client: AsyncClient):
    """PATCH /api/v1/products/{id} can set image_url via JSON update."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/products/{product_id}",
        json={"image_url": "data:image/png;base64,abc123"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["image_url"] == "data:image/png;base64,abc123"


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    """DELETE /api/v1/products/{id} removes the product."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/api/v1/products/{product_id}", headers=headers)
    assert del_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/products/{product_id}", headers=headers)
    assert get_resp.status_code == 404


# ── Image upload endpoint tests ──────────────────────────────


@pytest.mark.asyncio
async def test_upload_product_image(client: AsyncClient):
    """POST /api/v1/products/{id}/image stores image as base64 data URI."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    # Create a small fake PNG (1x1 pixel)
    fake_png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
    )
    file = io.BytesIO(fake_png)

    response = await client.post(
        f"/api/v1/products/{product_id}/image",
        files={"file": ("test.png", file, "image/png")},
        headers=headers,
    )
    assert response.status_code == 200

    data = response.json()
    assert data["image_url"] is not None
    assert data["image_url"].startswith("data:image/png;base64,")


@pytest.mark.asyncio
async def test_upload_product_image_invalid_type(client: AsyncClient):
    """POST /api/v1/products/{id}/image rejects non-image files."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    create_resp = await create_product(client, headers, tenant_id)
    product_id = create_resp.json()["id"]

    file = io.BytesIO(b"not an image")
    response = await client.post(
        f"/api/v1/products/{product_id}/image",
        files={"file": ("test.txt", file, "text/plain")},
        headers=headers,
    )
    assert response.status_code == 400
    assert "Invalid image type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_upload_product_image_not_found(client: AsyncClient):
    """POST /api/v1/products/{id}/image returns 404 for missing product."""
    headers = await get_auth_header(client)
    fake_id = "00000000-0000-0000-0000-000000000000"

    file = io.BytesIO(b"\x89PNG")
    response = await client.post(
        f"/api/v1/products/{fake_id}/image",
        files={"file": ("test.png", file, "image/png")},
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_image(client: AsyncClient):
    """DELETE /api/v1/products/{id}/image removes the image."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)

    # Create product with image
    payload = {
        **PRODUCT_PAYLOAD,
        "image_url": "data:image/png;base64,abc123",
    }
    create_resp = await create_product(client, headers, tenant_id, payload=payload)
    product_id = create_resp.json()["id"]
    assert create_resp.json()["image_url"] is not None

    # Delete image
    response = await client.delete(
        f"/api/v1/products/{product_id}/image",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["image_url"] is None
