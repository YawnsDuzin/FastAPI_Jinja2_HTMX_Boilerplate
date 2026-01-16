"""
Base Model Classes

모든 모델이 상속받는 기본 클래스와 믹스인 정의
"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TimestampMixin:
    """생성/수정 시간 자동 관리 믹스인"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """
    모든 모델의 기본 클래스

    자동으로 ID, 생성시간, 수정시간을 포함합니다.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def to_dict(self) -> dict[str, Any]:
        """모델을 딕셔너리로 변환"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """모델의 문자열 표현"""
        return f"<{self.__class__.__name__}(id={self.id})>"
