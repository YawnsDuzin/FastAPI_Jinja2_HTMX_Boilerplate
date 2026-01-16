"""
Database Configuration

SQLAlchemy 비동기 데이터베이스 연결 설정
세션 관리 및 의존성 주입 제공
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """SQLAlchemy 모델 베이스 클래스"""

    pass


# 비동기 엔진 생성
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# 비동기 세션 팩토리
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    데이터베이스 세션 의존성

    FastAPI의 Depends를 통해 사용되며, 요청 종료 시 자동으로 세션을 정리합니다.

    Yields:
        AsyncSession: 비동기 데이터베이스 세션
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """데이터베이스 테이블 초기화 (개발용)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """데이터베이스 연결 종료"""
    await engine.dispose()
