"""
Tests for the Combo Items CRUD endpoints, including image upload.
"""

import io

import pytest
from httpx import AsyncClient

from tests.test_auth import get_auth_header
from tests.test_products import create_product, setup_tenant


async def _create_combo_and_child(
    client: AsyncClient, headers: dict, tenant_id: str
) -> tuple[str, str]:
    """Helper: create a combo product and a child product, return their IDs."""
    combo_resp = await create_product(
        client,
        headers,
        tenant_id,
        payload={"name": "Combo Meal", "price": 12.99, "is_combo": True, "stock": 50},
    )
    child_resp = await create_product(
        client,
        headers,
        tenant_id,
        payload={"name": "Fries", "price": 2.99, "is_combo": False, "stock": 200},
    )
    return combo_resp.json()["id"], child_resp.json()["id"]


@pytest.mark.asyncio
async def test_create_combo_item(client: AsyncClient):
    """POST /api/v1/combo-items/ creates a combo item."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    response = await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 2},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["parent_id"] == parent_id
    assert data["child_id"] == child_id
    assert data["quantity"] == 2
    assert data["image_url"] is None


@pytest.mark.asyncio
async def test_create_combo_item_with_image_url(client: AsyncClient):
    """POST /api/v1/combo-items/ can include image_url at creation."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    response = await client.post(
        "/api/v1/combo-items/",
        json={
            "parent_id": parent_id,
            "child_id": child_id,
            "quantity": 1,
            "image_url": "data:image/png;base64,abc123",
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["image_url"] == "data:image/png;base64,abc123"


@pytest.mark.asyncio
async def test_list_combo_items_by_parent(client: AsyncClient):
    """GET /api/v1/combo-items/product/{id} returns combo items."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 1},
        headers=headers,
    )

    response = await client.get(
        f"/api/v1/combo-items/product/{parent_id}", headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_update_combo_item(client: AsyncClient):
    """PATCH /api/v1/combo-items/{id} updates the combo item."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    create_resp = await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 1},
        headers=headers,
    )
    combo_item_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/combo-items/{combo_item_id}",
        json={"quantity": 5},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


@pytest.mark.asyncio
async def test_update_combo_item_image_url(client: AsyncClient):
    """PATCH /api/v1/combo-items/{id} can set image_url via JSON update."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    create_resp = await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 1},
        headers=headers,
    )
    combo_item_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/combo-items/{combo_item_id}",
        json={"image_url": "data:image/png;base64,xyz789"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["image_url"] == "data:image/png;base64,xyz789"


@pytest.mark.asyncio
async def test_delete_combo_item(client: AsyncClient):
    """DELETE /api/v1/combo-items/{id} removes the combo item."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    create_resp = await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 1},
        headers=headers,
    )
    combo_item_id = create_resp.json()["id"]

    del_resp = await client.delete(
        f"/api/v1/combo-items/{combo_item_id}", headers=headers
    )
    assert del_resp.status_code == 204


# ── Image upload endpoint tests ──────────────────────────────


@pytest.mark.asyncio
async def test_upload_combo_item_image(client: AsyncClient):
    """POST /api/v1/combo-items/{id}/image stores image as base64 data URI."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    create_resp = await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 1},
        headers=headers,
    )
    combo_item_id = create_resp.json()["id"]

    # Create a small fake PNG
    fake_png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
    )
    file = io.BytesIO(fake_png)

    response = await client.post(
        f"/api/v1/combo-items/{combo_item_id}/image",
        files={"file": ("test.png", file, "image/png")},
        headers=headers,
    )
    assert response.status_code == 200

    data = response.json()
    assert data["image_url"] is not None
    assert data["image_url"].startswith("data:image/png;base64,")


@pytest.mark.asyncio
async def test_upload_combo_item_image_invalid_type(client: AsyncClient):
    """POST /api/v1/combo-items/{id}/image rejects non-image files."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    create_resp = await client.post(
        "/api/v1/combo-items/",
        json={"parent_id": parent_id, "child_id": child_id, "quantity": 1},
        headers=headers,
    )
    combo_item_id = create_resp.json()["id"]

    file = io.BytesIO(b"not an image")
    response = await client.post(
        f"/api/v1/combo-items/{combo_item_id}/image",
        files={"file": ("test.txt", file, "text/plain")},
        headers=headers,
    )
    assert response.status_code == 400
    assert "Invalid image type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_combo_item_image(client: AsyncClient):
    """DELETE /api/v1/combo-items/{id}/image removes the image."""
    headers = await get_auth_header(client)
    tenant_id = await setup_tenant(client, headers)
    parent_id, child_id = await _create_combo_and_child(client, headers, tenant_id)

    create_resp = await client.post(
        "/api/v1/combo-items/",
        json={
            "parent_id": parent_id,
            "child_id": child_id,
            "quantity": 1,
            "image_url": "data:image/png;base64,abc123",
        },
        headers=headers,
    )
    combo_item_id = create_resp.json()["id"]
    assert create_resp.json()["image_url"] is not None

    response = await client.delete(
        f"/api/v1/combo-items/{combo_item_id}/image",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["image_url"] is None
