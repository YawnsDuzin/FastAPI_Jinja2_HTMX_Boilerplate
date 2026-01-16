"""
User Service

사용자 관련 비즈니스 로직
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """사용자 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
    ) -> list[User]:
        """사용자 목록 조회"""
        query = select(User)

        if is_active is not None:
            query = query.where(User.is_active == is_active)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, user_in: UserCreate) -> User:
        """사용자 생성"""
        user = User(
            email=user_in.email,
            username=user_in.username,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user: User, user_in: UserUpdate) -> User:
        """사용자 정보 수정"""
        update_data = user_in.model_dump(exclude_unset=True)

        # 비밀번호가 있으면 해싱
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """사용자 삭제"""
        await self.db.delete(user)
        await self.db.flush()

    async def activate(self, user: User) -> User:
        """사용자 활성화"""
        user.is_active = True
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def deactivate(self, user: User) -> User:
        """사용자 비활성화"""
        user.is_active = False
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def verify(self, user: User) -> User:
        """사용자 인증 완료"""
        user.is_verified = True
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def is_email_taken(self, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """이메일 중복 확인"""
        query = select(User).where(User.email == email)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def is_username_taken(
        self, username: str, exclude_user_id: Optional[int] = None
    ) -> bool:
        """사용자명 중복 확인"""
        query = select(User).where(User.username == username)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
