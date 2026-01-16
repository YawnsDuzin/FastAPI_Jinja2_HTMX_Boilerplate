"""
Item Model

샘플 아이템 모델 - CRUD 예제용
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Item(BaseModel):
    """아이템 모델 (CRUD 예제)"""

    __tablename__ = "items"

    # 기본 정보
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # 상태
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    priority: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # 소유자 관계
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="items",
    )

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title={self.title})>"
