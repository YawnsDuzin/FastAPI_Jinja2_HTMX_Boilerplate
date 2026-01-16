"""
Item Schemas

아이템 관련 Pydantic 스키마 정의
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """아이템 기본 스키마"""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(default=0, ge=0, le=10)


class ItemCreate(ItemBase):
    """아이템 생성 스키마"""

    pass


class ItemUpdate(BaseModel):
    """아이템 수정 스키마"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=0, le=10)
    is_active: Optional[bool] = None


class Item(ItemBase):
    """아이템 응답 스키마"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime


class ItemWithOwner(Item):
    """소유자 정보 포함 아이템 스키마"""

    from app.schemas.user import User

    owner: User
