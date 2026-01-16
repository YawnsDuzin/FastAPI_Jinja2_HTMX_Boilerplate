"""
API Dependencies

FastAPI 의존성 주입 함수 정의
"""

from typing import Annotated, Optional

from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.database import get_db
from app.models.user import User
from app.services.auth import AuthService
from app.services.item import ItemService
from app.services.user import UserService

# Database Session
DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_token_from_cookie(
    access_token: Annotated[Optional[str], Cookie()] = None,
) -> Optional[str]:
    """쿠키에서 토큰 추출"""
    return access_token


async def get_current_user(
    db: DbSession,
    token: Annotated[Optional[str], Depends(get_token_from_cookie)],
) -> User:
    """
    현재 인증된 사용자 조회

    쿠키에서 JWT 토큰을 추출하여 사용자를 인증합니다.

    Raises:
        HTTPException: 인증 실패 시 401 에러
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(token, token_type="access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = int(payload["sub"])
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비활성화된 계정입니다.",
        )

    return user


async def get_current_user_optional(
    db: DbSession,
    token: Annotated[Optional[str], Depends(get_token_from_cookie)],
) -> Optional[User]:
    """
    현재 사용자 조회 (선택적)

    인증이 필수가 아닌 엔드포인트에서 사용합니다.
    토큰이 없거나 유효하지 않으면 None을 반환합니다.
    """
    if not token:
        return None

    payload = verify_token(token, token_type="access")
    if not payload:
        return None

    user_id = int(payload["sub"])
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user or not user.is_active:
        return None

    return user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    현재 슈퍼유저 조회

    Raises:
        HTTPException: 슈퍼유저가 아닐 경우 403 에러
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    return current_user


# Type Aliases for Dependency Injection
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[Optional[User], Depends(get_current_user_optional)]
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]


# Service Dependencies
def get_user_service(db: DbSession) -> UserService:
    """UserService 의존성"""
    return UserService(db)


def get_auth_service(db: DbSession) -> AuthService:
    """AuthService 의존성"""
    return AuthService(db)


def get_item_service(db: DbSession) -> ItemService:
    """ItemService 의존성"""
    return ItemService(db)
