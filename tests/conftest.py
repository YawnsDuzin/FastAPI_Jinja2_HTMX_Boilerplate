"""
Pytest Configuration and Fixtures

테스트 설정 및 공통 픽스처 정의
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash


# 테스트용 데이터베이스 URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 테스트용 엔진 생성
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

# 테스트용 세션 팩토리
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """이벤트 루프 픽스처"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """테스트용 데이터베이스 세션"""
    # 테이블 생성
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    # 테이블 삭제
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """테스트용 HTTP 클라이언트"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """테스트용 사용자 생성"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, test_user: User) -> AsyncClient:
    """인증된 테스트 클라이언트"""
    # 로그인
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200

    # 쿠키 설정
    client.cookies = response.cookies
    return client
