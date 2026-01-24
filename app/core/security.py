"""
Security Utilities

JWT 토큰 생성/검증, 비밀번호 해싱 등 보안 관련 유틸리티
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
from jose import JWTError, jwt

from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 해시된 비밀번호 비교

    Args:
        plain_password: 평문 비밀번호
        hashed_password: 해시된 비밀번호

    Returns:
        비밀번호 일치 여부
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    """
    비밀번호 해싱

    Args:
        password: 평문 비밀번호

    Returns:
        해시된 비밀번호
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
    extra_data: Optional[dict[str, Any]] = None,
) -> str:
    """
    JWT 액세스 토큰 생성

    Args:
        subject: 토큰 주체 (일반적으로 사용자 ID)
        expires_delta: 만료 시간 (기본값: 설정의 JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        extra_data: 토큰에 포함할 추가 데이터

    Returns:
        인코딩된 JWT 토큰
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    if extra_data:
        to_encode.update(extra_data)

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def create_refresh_token(subject: str | int) -> str:
    """
    JWT 리프레시 토큰 생성

    Args:
        subject: 토큰 주체 (일반적으로 사용자 ID)

    Returns:
        인코딩된 JWT 리프레시 토큰
    """
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict[str, Any]]:
    """
    JWT 토큰 검증

    Args:
        token: 검증할 JWT 토큰
        token_type: 토큰 타입 ("access" 또는 "refresh")

    Returns:
        토큰 페이로드 또는 None (검증 실패 시)
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        # 토큰 타입 검증
        if payload.get("type") != token_type:
            return None

        return payload
    except JWTError:
        return None


def generate_csrf_token() -> str:
    """CSRF 토큰 생성"""
    import secrets

    return secrets.token_urlsafe(32)
