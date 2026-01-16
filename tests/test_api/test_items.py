"""
Items API Tests

아이템 CRUD API 테스트
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item


@pytest.fixture
async def test_item(db_session: AsyncSession, test_user) -> Item:
    """테스트용 아이템 생성"""
    item = Item(
        title="Test Item",
        description="Test Description",
        priority=5,
        owner_id=test_user.id,
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item


@pytest.mark.asyncio
async def test_create_item(auth_client: AsyncClient):
    """아이템 생성 테스트"""
    response = await auth_client.post(
        "/api/v1/items",
        json={
            "title": "New Item",
            "description": "New Description",
            "priority": 3,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Item"
    assert data["description"] == "New Description"
    assert data["priority"] == 3
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_get_items(auth_client: AsyncClient, test_item):
    """아이템 목록 조회 테스트"""
    response = await auth_client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_item(auth_client: AsyncClient, test_item):
    """아이템 상세 조회 테스트"""
    response = await auth_client.get(f"/api/v1/items/{test_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_item.title
    assert data["id"] == test_item.id


@pytest.mark.asyncio
async def test_update_item(auth_client: AsyncClient, test_item):
    """아이템 수정 테스트"""
    response = await auth_client.patch(
        f"/api/v1/items/{test_item.id}",
        json={"title": "Updated Title"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_item(auth_client: AsyncClient, test_item):
    """아이템 삭제 테스트"""
    response = await auth_client.delete(f"/api/v1/items/{test_item.id}")
    assert response.status_code == 200

    # 삭제 확인
    response = await auth_client.get(f"/api/v1/items/{test_item.id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_toggle_item(auth_client: AsyncClient, test_item):
    """아이템 토글 테스트"""
    original_status = test_item.is_active

    response = await auth_client.post(f"/api/v1/items/{test_item.id}/toggle")
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] != original_status


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """인증되지 않은 접근 테스트"""
    response = await client.get("/api/v1/items")
    assert response.status_code == 401
