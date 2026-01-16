"""
Auth API Tests

인증 관련 API 테스트
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """회원가입 테스트"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user):
    """중복 이메일 회원가입 테스트"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",  # 이미 존재하는 이메일
            "username": "anotheruser",
            "password": "password123",
        },
    )
    assert response.status_code == 409  # Conflict


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    """로그인 테스트"""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    # 쿠키 확인
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    """잘못된 비밀번호 로그인 테스트"""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(auth_client: AsyncClient, test_user):
    """현재 사용자 조회 테스트"""
    response = await auth_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_logout(auth_client: AsyncClient):
    """로그아웃 테스트"""
    response = await auth_client.post("/api/v1/auth/logout")
    assert response.status_code == 200

    # 쿠키가 삭제되었는지 확인
    assert response.cookies.get("access_token") is None or response.cookies.get("access_token") == ""
