"""
Common Schemas

공통으로 사용되는 스키마 정의
"""

from typing import Any, Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class Message(BaseModel):
    """간단한 메시지 응답 스키마"""

    message: str


class PaginatedResponse(BaseModel, Generic[T]):
    """페이지네이션 응답 스키마"""

    model_config = ConfigDict(from_attributes=True)

    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int,
    ) -> "PaginatedResponse[T]":
        """페이지네이션 응답 생성"""
        pages = (total + size - 1) // size if size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
        )


class HealthCheck(BaseModel):
    """헬스 체크 응답 스키마"""

    status: str
    app: str


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""

    error: bool = True
    message: str
    detail: dict[str, Any] | None = None
