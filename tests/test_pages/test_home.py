"""
Home Page Tests

홈페이지 관련 테스트
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_home_page(client: AsyncClient):
    """홈페이지 접근 테스트"""
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FastAPI" in response.text or "보일러플레이트" in response.text


@pytest.mark.asyncio
async def test_about_page(client: AsyncClient):
    """소개 페이지 접근 테스트"""
    response = await client.get("/about")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_login_page(client: AsyncClient):
    """로그인 페이지 접근 테스트"""
    response = await client.get("/login")
    assert response.status_code == 200
    assert "로그인" in response.text


@pytest.mark.asyncio
async def test_register_page(client: AsyncClient):
    """회원가입 페이지 접근 테스트"""
    response = await client.get("/register")
    assert response.status_code == 200
    assert "회원가입" in response.text


@pytest.mark.asyncio
async def test_dashboard_redirect(client: AsyncClient):
    """대시보드 페이지 인증 없이 접근 테스트"""
    response = await client.get("/dashboard", follow_redirects=False)
    # 인증이 필요한 페이지는 401 또는 리다이렉트
    assert response.status_code in [401, 302, 303]


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """헬스 체크 엔드포인트 테스트"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
