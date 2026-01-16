"""
User Schemas

사용자 관련 Pydantic 스키마 정의
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """사용자 기본 스키마"""

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """사용자 생성 스키마"""

    password: str = Field(min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """사용자 수정 스키마"""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class User(UserBase):
    """사용자 응답 스키마"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    avatar_url: Optional[str] = None
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    """로그인 요청 스키마"""

    email: EmailStr
    password: str


class Token(BaseModel):
    """토큰 응답 스키마"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """토큰 페이로드 스키마"""

    sub: str
    exp: int
    type: str


class PasswordChange(BaseModel):
    """비밀번호 변경 스키마"""

    current_password: str
    new_password: str = Field(min_length=8, max_length=100)
