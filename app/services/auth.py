"""
Auth Service

인증 관련 비즈니스 로직
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, ConflictError, ValidationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.models.user import User
from app.schemas.user import Token, UserCreate
from app.services.user import UserService


class AuthService:
    """인증 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)

    async def register(self, user_in: UserCreate) -> User:
        """
        회원가입

        Args:
            user_in: 사용자 생성 데이터

        Returns:
            생성된 사용자

        Raises:
            ConflictError: 이메일 또는 사용자명이 이미 존재할 경우
        """
        # 이메일 중복 확인
        if await self.user_service.is_email_taken(user_in.email):
            raise ConflictError("이미 등록된 이메일입니다.")

        # 사용자명 중복 확인
        if await self.user_service.is_username_taken(user_in.username):
            raise ConflictError("이미 사용중인 사용자명입니다.")

        # 사용자 생성
        user = await self.user_service.create(user_in)
        return user

    async def login(self, email: str, password: str) -> Token:
        """
        로그인

        Args:
            email: 이메일
            password: 비밀번호

        Returns:
            JWT 토큰

        Raises:
            AuthenticationError: 인증 실패
        """
        # 사용자 조회
        user = await self.user_service.get_by_email(email)
        if not user:
            raise AuthenticationError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # 비밀번호 검증
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # 활성 상태 확인
        if not user.is_active:
            raise AuthenticationError("비활성화된 계정입니다.")

        # 토큰 생성
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_tokens(self, refresh_token: str) -> Token:
        """
        토큰 갱신

        Args:
            refresh_token: 리프레시 토큰

        Returns:
            새로운 JWT 토큰

        Raises:
            AuthenticationError: 토큰 검증 실패
        """
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise AuthenticationError("유효하지 않은 토큰입니다.")

        user_id = int(payload["sub"])
        user = await self.user_service.get_by_id(user_id)

        if not user or not user.is_active:
            raise AuthenticationError("사용자를 찾을 수 없거나 비활성화된 계정입니다.")

        # 새 토큰 생성
        new_access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        현재 사용자 조회

        Args:
            token: JWT 액세스 토큰

        Returns:
            사용자 또는 None
        """
        payload = verify_token(token, token_type="access")
        if not payload:
            return None

        user_id = int(payload["sub"])
        user = await self.user_service.get_by_id(user_id)

        if not user or not user.is_active:
            return None

        return user

    async def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> User:
        """
        비밀번호 변경

        Args:
            user: 사용자
            current_password: 현재 비밀번호
            new_password: 새 비밀번호

        Returns:
            수정된 사용자

        Raises:
            ValidationError: 현재 비밀번호 불일치
        """
        if not verify_password(current_password, user.hashed_password):
            raise ValidationError("현재 비밀번호가 올바르지 않습니다.")

        user.hashed_password = get_password_hash(new_password)
        await self.db.flush()
        await self.db.refresh(user)
        return user
