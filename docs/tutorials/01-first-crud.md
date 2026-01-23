# 🚀 첫 번째 CRUD 기능 만들기

이 튜토리얼에서는 "할 일 목록(Todo)" 기능을 처음부터 끝까지 만들어봅니다.
완료하면 이 보일러플레이트의 구조와 각 기술 스택의 역할을 이해할 수 있습니다.

## 📋 목차

1. [개요](#1-개요)
2. [Step 1: 데이터베이스 모델 생성](#step-1-데이터베이스-모델-생성)
3. [Step 2: Pydantic 스키마 생성](#step-2-pydantic-스키마-생성)
4. [Step 3: 서비스 레이어 생성](#step-3-서비스-레이어-생성)
5. [Step 4: API 라우터 생성](#step-4-api-라우터-생성)
6. [Step 5: 페이지 라우터 생성](#step-5-페이지-라우터-생성)
7. [Step 6: HTMX 파셜 라우터 생성](#step-6-htmx-파셜-라우터-생성)
8. [Step 7: 템플릿 생성](#step-7-템플릿-생성)
9. [Step 8: 라우터 등록](#step-8-라우터-등록)
10. [Step 9: 테스트](#step-9-테스트)
11. [완성된 코드 요약](#완성된-코드-요약)

---

## 1. 개요

### 만들 기능

- **Todo 목록 보기**: 모든 할 일 표시
- **Todo 추가**: 새로운 할 일 입력
- **Todo 완료 토글**: 체크박스로 완료 표시
- **Todo 삭제**: 할 일 삭제

### 파일 구조

```
app/
├── models/
│   └── todo.py          # 데이터베이스 모델
├── schemas/
│   └── todo.py          # Pydantic 스키마
├── services/
│   └── todo.py          # 비즈니스 로직
├── api/v1/
│   └── todos.py         # REST API 엔드포인트
├── pages/
│   └── todos.py         # HTML 페이지 라우터
└── partials/
    └── todos.py         # HTMX 파셜 라우터

templates/
├── pages/
│   └── todos.html       # 메인 페이지
└── partials/
    └── todos/
        ├── list.html    # 목록 파셜
        ├── item.html    # 개별 아이템 파셜
        └── form.html    # 입력 폼 파셜
```

---

## Step 1: 데이터베이스 모델 생성

데이터베이스 모델은 테이블 구조를 정의합니다.

### `app/models/todo.py` 생성

```python
"""
Todo Model - 할 일 데이터베이스 모델

SQLAlchemy ORM을 사용하여 todos 테이블을 정의합니다.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Todo(BaseModel):
    """
    할 일 모델

    Attributes:
        id: 고유 식별자 (자동 생성)
        title: 할 일 제목 (필수)
        description: 상세 설명 (선택)
        is_completed: 완료 여부 (기본값: False)
        owner_id: 소유자 사용자 ID (외래키)
        owner: 소유자 User 객체 (관계)

    BaseModel 상속:
        - created_at: 생성 시간 (자동)
        - updated_at: 수정 시간 (자동)
    """

    # ==========================================================================
    # 테이블 설정
    # ==========================================================================
    __tablename__ = "todos"  # 실제 DB 테이블 이름

    # ==========================================================================
    # 컬럼 정의
    # ==========================================================================
    # Column(타입, 옵션들...)
    # - nullable=False: NOT NULL 제약조건
    # - default=값: 기본값 설정
    # - index=True: 인덱스 생성 (검색 성능 향상)

    title = Column(
        String(200),        # VARCHAR(200)
        nullable=False,     # 필수 입력
        index=True,         # 제목으로 검색할 수 있도록 인덱스 생성
    )

    description = Column(
        Text,               # TEXT 타입 (긴 문자열)
        nullable=True,      # 선택 입력
    )

    is_completed = Column(
        Boolean,            # BOOLEAN
        default=False,      # 기본값: 미완료
        nullable=False,
    )

    # ==========================================================================
    # 외래키 (Foreign Key)
    # ==========================================================================
    # ForeignKey("테이블명.컬럼명")으로 다른 테이블과 연결
    # ondelete="CASCADE": 사용자 삭제 시 관련 Todo도 삭제

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ==========================================================================
    # 관계 (Relationship)
    # ==========================================================================
    # relationship: ORM에서 관련 객체를 자동으로 로드
    # back_populates: 양방향 관계 설정 (User 모델에도 todos 관계 추가 필요)

    owner = relationship(
        "User",                      # 연결할 모델 이름
        back_populates="todos",      # User.todos와 연결
    )

    def __repr__(self) -> str:
        """디버깅용 문자열 표현"""
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.is_completed})>"
```

### User 모델에 관계 추가

`app/models/user.py` 파일에 todos 관계를 추가합니다:

```python
# 기존 import 아래에 추가
from sqlalchemy.orm import relationship

class User(BaseModel):
    # ... 기존 코드 ...

    # 관계 추가 (클래스 내부 마지막에)
    todos = relationship(
        "Todo",
        back_populates="owner",
        cascade="all, delete-orphan",  # User 삭제 시 Todo도 삭제
    )
```

### 모델 등록

`app/models/__init__.py`에 모델 추가:

```python
from app.models.base import BaseModel
from app.models.user import User
from app.models.item import Item
from app.models.todo import Todo  # 추가

__all__ = ["BaseModel", "User", "Item", "Todo"]
```

---

## Step 2: Pydantic 스키마 생성

스키마는 API 요청/응답 데이터의 형식을 정의하고 검증합니다.

### `app/schemas/todo.py` 생성

```python
"""
Todo Schemas - 할 일 데이터 검증 스키마

Pydantic을 사용하여 입력 데이터 검증과 응답 형식을 정의합니다.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# 기본 스키마 (Base)
# =============================================================================
# 다른 스키마들이 공통으로 사용하는 필드 정의

class TodoBase(BaseModel):
    """
    Todo 기본 스키마

    다른 스키마들이 상속받아 사용합니다.
    공통 필드인 title과 description을 정의합니다.
    """
    title: str = Field(
        ...,                              # ... = 필수 필드
        min_length=1,                     # 최소 1글자
        max_length=200,                   # 최대 200글자
        description="할 일 제목",
        examples=["장보기", "운동하기"],   # API 문서 예시
    )
    description: Optional[str] = Field(
        None,                             # None = 선택 필드
        max_length=1000,
        description="상세 설명",
    )


# =============================================================================
# 생성용 스키마 (Create)
# =============================================================================
# API로 새 Todo를 생성할 때 사용

class TodoCreate(TodoBase):
    """
    Todo 생성 스키마

    POST /api/v1/todos 요청 바디에 사용됩니다.
    TodoBase의 title, description을 상속받습니다.
    """
    pass  # 추가 필드 없음, TodoBase 그대로 사용


# =============================================================================
# 수정용 스키마 (Update)
# =============================================================================
# API로 Todo를 수정할 때 사용

class TodoUpdate(BaseModel):
    """
    Todo 수정 스키마

    PATCH /api/v1/todos/{id} 요청 바디에 사용됩니다.
    모든 필드가 Optional이므로 변경하고 싶은 필드만 전송하면 됩니다.
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
    )
    is_completed: Optional[bool] = None


# =============================================================================
# 응답용 스키마 (Response)
# =============================================================================
# API 응답에 사용

class Todo(TodoBase):
    """
    Todo 응답 스키마

    API 응답에서 Todo 객체를 직렬화할 때 사용됩니다.

    ConfigDict 설정:
        from_attributes=True: SQLAlchemy 모델을 Pydantic 모델로 변환 가능
        (이전 버전의 orm_mode=True와 동일)
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_completed: bool = False
    owner_id: int
    created_at: datetime
    updated_at: datetime


# =============================================================================
# 목록 응답 스키마
# =============================================================================

class TodoList(BaseModel):
    """
    Todo 목록 응답 스키마

    페이지네이션 정보와 함께 Todo 목록을 반환합니다.
    """
    items: list[Todo]
    total: int
    completed_count: int      # 완료된 항목 수
    pending_count: int        # 미완료 항목 수
```

---

## Step 3: 서비스 레이어 생성

서비스 레이어는 비즈니스 로직을 담당합니다.

### `app/services/todo.py` 생성

```python
"""
Todo Service - 할 일 비즈니스 로직

데이터베이스 작업을 추상화하고 비즈니스 규칙을 적용합니다.
"""

from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    """
    할 일 서비스

    Todo 관련 모든 비즈니스 로직을 처리합니다.
    라우터에서 직접 DB 작업을 하지 않고 서비스를 통해 처리합니다.

    왜 서비스 레이어를 사용하나요?
        1. 재사용성: 같은 로직을 여러 곳에서 사용
        2. 테스트 용이: 서비스 단위로 테스트 가능
        3. 관심사 분리: 라우터는 HTTP 처리, 서비스는 비즈니스 로직
        4. 유지보수: 비즈니스 로직 변경 시 서비스만 수정
    """

    def __init__(self, db: AsyncSession):
        """
        서비스 초기화

        Args:
            db: 데이터베이스 세션 (요청마다 새로 생성됨)
        """
        self.db = db

    # =========================================================================
    # 조회 (Read)
    # =========================================================================

    async def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        ID로 Todo 조회

        Args:
            todo_id: 조회할 Todo ID

        Returns:
            Todo 객체 또는 None (없으면)
        """
        # select(): SQL SELECT 문 생성
        # where(): WHERE 조건 추가
        query = select(Todo).where(Todo.id == todo_id)

        # execute(): 쿼리 실행
        # scalar_one_or_none(): 결과 1개 또는 None 반환
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_todos(
        self,
        user_id: int,
        is_completed: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Todo]:
        """
        사용자의 Todo 목록 조회

        Args:
            user_id: 사용자 ID
            is_completed: 완료 여부 필터 (None이면 전체)
            skip: 건너뛸 개수 (페이지네이션)
            limit: 가져올 개수 (페이지네이션)

        Returns:
            Todo 목록
        """
        query = select(Todo).where(Todo.owner_id == user_id)

        # 완료 여부 필터
        if is_completed is not None:
            query = query.where(Todo.is_completed == is_completed)

        # 정렬: 미완료 먼저, 최신순
        query = query.order_by(Todo.is_completed, Todo.created_at.desc())

        # 페이지네이션
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()  # 모든 결과를 리스트로

    async def get_user_todo_counts(self, user_id: int) -> dict:
        """
        사용자의 Todo 통계 조회

        Args:
            user_id: 사용자 ID

        Returns:
            dict: {total, completed_count, pending_count}
        """
        # 완료된 항목 수
        completed_query = select(func.count(Todo.id)).where(
            Todo.owner_id == user_id,
            Todo.is_completed == True,
        )
        completed_result = await self.db.execute(completed_query)
        completed_count = completed_result.scalar() or 0

        # 미완료 항목 수
        pending_query = select(func.count(Todo.id)).where(
            Todo.owner_id == user_id,
            Todo.is_completed == False,
        )
        pending_result = await self.db.execute(pending_query)
        pending_count = pending_result.scalar() or 0

        return {
            "total": completed_count + pending_count,
            "completed_count": completed_count,
            "pending_count": pending_count,
        }

    # =========================================================================
    # 생성 (Create)
    # =========================================================================

    async def create(self, user: User, todo_in: TodoCreate) -> Todo:
        """
        새 Todo 생성

        Args:
            user: 소유자 User 객체
            todo_in: 생성할 Todo 데이터

        Returns:
            생성된 Todo 객체

        작동 흐름:
            1. Todo 인스턴스 생성
            2. DB 세션에 추가
            3. flush로 DB에 전송 (아직 커밋 아님)
            4. refresh로 DB에서 최신 데이터 로드 (id, created_at 등)
        """
        # model_dump(): Pydantic 모델을 딕셔너리로 변환
        todo = Todo(
            **todo_in.model_dump(),  # title, description
            owner_id=user.id,        # 소유자 설정
        )

        self.db.add(todo)            # 세션에 추가
        await self.db.flush()        # DB에 전송 (INSERT 실행)
        await self.db.refresh(todo)  # 생성된 데이터 로드

        return todo

    # =========================================================================
    # 수정 (Update)
    # =========================================================================

    async def update(self, todo: Todo, todo_in: TodoUpdate) -> Todo:
        """
        Todo 수정

        Args:
            todo: 수정할 Todo 객체
            todo_in: 수정 데이터

        Returns:
            수정된 Todo 객체
        """
        # exclude_unset=True: 설정되지 않은 필드 제외
        # (None으로 명시적 설정한 것과 아예 안 보낸 것을 구분)
        update_data = todo_in.model_dump(exclude_unset=True)

        # 각 필드 업데이트
        for field, value in update_data.items():
            setattr(todo, field, value)

        await self.db.flush()
        await self.db.refresh(todo)

        return todo

    async def toggle_completed(self, todo: Todo) -> Todo:
        """
        완료 상태 토글

        Args:
            todo: 토글할 Todo 객체

        Returns:
            수정된 Todo 객체
        """
        todo.is_completed = not todo.is_completed
        await self.db.flush()
        await self.db.refresh(todo)
        return todo

    # =========================================================================
    # 삭제 (Delete)
    # =========================================================================

    async def delete(self, todo: Todo) -> None:
        """
        Todo 삭제

        Args:
            todo: 삭제할 Todo 객체
        """
        await self.db.delete(todo)
        await self.db.flush()
```

---

## Step 4: API 라우터 생성

REST API 엔드포인트를 정의합니다.

### `app/api/v1/todos.py` 생성

```python
"""
Todos API Router - 할 일 REST API

JSON 응답을 반환하는 REST API 엔드포인트입니다.
외부 클라이언트(모바일 앱 등)에서 사용할 수 있습니다.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.todo import Todo, TodoCreate, TodoList, TodoUpdate
from app.services.todo import TodoService

# =============================================================================
# 라우터 설정
# =============================================================================
# prefix: 이 라우터의 모든 경로 앞에 붙는 접두사
# tags: API 문서에서 그룹화할 태그

router = APIRouter(prefix="/todos", tags=["todos"])


# =============================================================================
# 의존성 함수
# =============================================================================

def get_todo_service(db: DbSession) -> TodoService:
    """TodoService 의존성 주입"""
    return TodoService(db)


# =============================================================================
# 엔드포인트
# =============================================================================

@router.get("", response_model=TodoList)
async def list_todos(
    is_completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
) -> TodoList:
    """
    Todo 목록 조회

    현재 로그인한 사용자의 Todo 목록을 반환합니다.

    Query Parameters:
        is_completed: True(완료) / False(미완료) / 생략(전체)
        skip: 건너뛸 개수 (기본: 0)
        limit: 가져올 개수 (기본: 100)
    """
    todos = await service.get_user_todos(
        user_id=current_user.id,
        is_completed=is_completed,
        skip=skip,
        limit=limit,
    )
    counts = await service.get_user_todo_counts(current_user.id)

    return TodoList(
        items=todos,
        **counts,
    )


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_in: TodoCreate,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
) -> Todo:
    """
    새 Todo 생성

    Request Body:
        title: 제목 (필수)
        description: 설명 (선택)
    """
    todo = await service.create(current_user, todo_in)
    return todo


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: int,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
) -> Todo:
    """
    Todo 상세 조회

    Path Parameters:
        todo_id: 조회할 Todo ID
    """
    todo = await service.get_by_id(todo_id)

    # 존재하지 않으면 404
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )

    # 다른 사용자의 Todo 접근 시 403
    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="접근 권한이 없습니다.",
        )

    return todo


@router.patch("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
) -> Todo:
    """
    Todo 수정

    Path Parameters:
        todo_id: 수정할 Todo ID

    Request Body:
        title: 제목 (선택)
        description: 설명 (선택)
        is_completed: 완료 여부 (선택)
    """
    todo = await service.get_by_id(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )

    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="접근 권한이 없습니다.",
        )

    return await service.update(todo, todo_in)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
) -> None:
    """
    Todo 삭제

    Path Parameters:
        todo_id: 삭제할 Todo ID
    """
    todo = await service.get_by_id(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )

    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="접근 권한이 없습니다.",
        )

    await service.delete(todo)
```

---

## Step 5: 페이지 라우터 생성

HTML 페이지를 렌더링하는 라우터입니다.

### `app/pages/todos.py` 생성

```python
"""
Todos Page Router - 할 일 페이지 라우터

HTML 페이지를 렌더링합니다.
"""

from fastapi import APIRouter, Depends, Request

from app.api.deps import CurrentUser, DbSession
from app.core.templates import templates
from app.services.todo import TodoService

router = APIRouter(tags=["pages"])


def get_todo_service(db: DbSession) -> TodoService:
    return TodoService(db)


@router.get("/todos")
async def todos_page(
    request: Request,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
):
    """
    Todo 메인 페이지

    사용자의 Todo 목록을 보여주는 페이지입니다.
    """
    # 사용자의 Todo 목록 조회
    todos = await service.get_user_todos(current_user.id)
    counts = await service.get_user_todo_counts(current_user.id)

    # 템플릿 렌더링
    return templates.TemplateResponse(
        request=request,
        name="pages/todos.html",
        context={
            "todos": todos,
            "total": counts["total"],
            "completed_count": counts["completed_count"],
            "pending_count": counts["pending_count"],
        },
    )
```

---

## Step 6: HTMX 파셜 라우터 생성

HTMX 요청에 대해 부분 HTML을 반환하는 라우터입니다.

### `app/partials/todos.py` 생성

```python
"""
Todos Partial Router - 할 일 파셜 라우터

HTMX 요청에 대해 부분 HTML을 반환합니다.
페이지 전체를 새로고침하지 않고 특정 영역만 업데이트합니다.
"""

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from app.api.deps import CurrentUser, DbSession
from app.core.templates import templates
from app.schemas.todo import TodoCreate
from app.services.todo import TodoService

router = APIRouter(prefix="/todos", tags=["partials"])


def get_todo_service(db: DbSession) -> TodoService:
    return TodoService(db)


# =============================================================================
# 목록 파셜
# =============================================================================

@router.get("/list", response_class=HTMLResponse)
async def todo_list_partial(
    request: Request,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
):
    """
    Todo 목록 파셜

    HTMX로 목록을 갱신할 때 사용합니다.
    """
    todos = await service.get_user_todos(current_user.id)
    counts = await service.get_user_todo_counts(current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="partials/todos/list.html",
        context={
            "todos": todos,
            "total": counts["total"],
            "completed_count": counts["completed_count"],
            "pending_count": counts["pending_count"],
        },
    )


# =============================================================================
# 생성 파셜
# =============================================================================

@router.post("/create", response_class=HTMLResponse)
async def create_todo_partial(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
):
    """
    새 Todo 생성 파셜

    폼 제출 후 생성된 아이템의 HTML을 반환합니다.
    hx-swap="afterbegin"과 함께 사용하면 목록 맨 위에 추가됩니다.
    """
    # 폼 데이터를 스키마로 변환
    todo_in = TodoCreate(title=title, description=description)

    # 생성
    todo = await service.create(current_user, todo_in)

    # 생성된 아이템 HTML 반환
    return templates.TemplateResponse(
        request=request,
        name="partials/todos/item.html",
        context={"todo": todo},
        # HTMX 헤더로 토스트 알림 트리거
        headers={
            "HX-Trigger": '{"showToast": {"type": "success", "message": "할 일이 추가되었습니다."}}',
        },
    )


# =============================================================================
# 토글 파셜
# =============================================================================

@router.post("/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo_partial(
    request: Request,
    todo_id: int,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
):
    """
    Todo 완료 토글 파셜

    체크박스 클릭 시 완료 상태를 토글하고 업데이트된 아이템을 반환합니다.
    hx-swap="outerHTML"로 아이템 전체를 교체합니다.
    """
    todo = await service.get_by_id(todo_id)

    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    todo = await service.toggle_completed(todo)

    return templates.TemplateResponse(
        request=request,
        name="partials/todos/item.html",
        context={"todo": todo},
    )


# =============================================================================
# 삭제 파셜
# =============================================================================

@router.delete("/{todo_id}", response_class=HTMLResponse)
async def delete_todo_partial(
    request: Request,
    todo_id: int,
    current_user: CurrentUser = None,
    service: TodoService = Depends(get_todo_service),
):
    """
    Todo 삭제 파셜

    삭제 후 빈 응답을 반환합니다.
    hx-swap="delete"로 해당 아이템을 DOM에서 제거합니다.
    """
    todo = await service.get_by_id(todo_id)

    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await service.delete(todo)

    # 빈 응답 + 토스트 알림
    return HTMLResponse(
        content="",
        headers={
            "HX-Trigger": '{"showToast": {"type": "info", "message": "할 일이 삭제되었습니다."}}',
        },
    )
```

---

## Step 7: 템플릿 생성

### 7.1 메인 페이지 템플릿

`templates/pages/todos.html`:

```html
{% extends "base.html" %}

{% block title %}할 일 목록{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <!-- 헤더 -->
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            할 일 목록
        </h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
            완료: {{ completed_count }} / 전체: {{ total }}
        </p>
    </div>

    <!-- 입력 폼 -->
    <!--
    HTMX 속성 설명:
    - hx-post: POST 요청을 보낼 URL
    - hx-target: 응답을 넣을 요소
    - hx-swap: 응답을 어떻게 넣을지 (afterbegin = 맨 앞에 추가)
    - hx-on::after-request: 요청 완료 후 실행할 코드
    -->
    <form hx-post="/partials/todos/create"
          hx-target="#todo-list"
          hx-swap="afterbegin"
          hx-on::after-request="this.reset()"
          class="mb-6">
        <div class="flex gap-2">
            <input type="text"
                   name="title"
                   required
                   placeholder="새로운 할 일..."
                   class="flex-1 rounded-lg border border-gray-300 dark:border-gray-600
                          bg-white dark:bg-gray-800 px-4 py-2
                          focus:ring-2 focus:ring-primary-500 focus:border-transparent">
            <button type="submit"
                    class="px-6 py-2 bg-primary-500 text-white rounded-lg
                           hover:bg-primary-600 transition-colors">
                추가
            </button>
        </div>
    </form>

    <!-- Todo 목록 -->
    <div id="todo-list" class="space-y-2">
        {% for todo in todos %}
            {% include "partials/todos/item.html" %}
        {% else %}
            <p class="text-center text-gray-500 py-8">
                할 일이 없습니다. 새로운 할 일을 추가해보세요!
            </p>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### 7.2 아이템 파셜 템플릿

`templates/partials/todos/item.html`:

```html
<!--
Todo 아이템 파셜

단일 Todo 항목을 렌더링합니다.
HTMX로 개별 아이템을 업데이트하거나 삭제할 때 사용됩니다.
-->
<div id="todo-{{ todo.id }}"
     class="flex items-center gap-4 p-4 bg-white dark:bg-gray-800
            rounded-lg shadow-sm border border-gray-200 dark:border-gray-700
            {{ 'opacity-60' if todo.is_completed else '' }}">

    <!-- 체크박스: 클릭 시 토글 -->
    <!--
    hx-post: 토글 요청
    hx-swap="outerHTML": 이 아이템 전체를 응답으로 교체
    -->
    <button hx-post="/partials/todos/{{ todo.id }}/toggle"
            hx-swap="outerHTML"
            hx-target="#todo-{{ todo.id }}"
            class="flex-shrink-0 w-6 h-6 rounded-full border-2
                   {{ 'bg-primary-500 border-primary-500' if todo.is_completed
                      else 'border-gray-300 dark:border-gray-600' }}
                   hover:border-primary-400 transition-colors">
        {% if todo.is_completed %}
            <!-- 체크 아이콘 -->
            <svg class="w-full h-full text-white p-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
            </svg>
        {% endif %}
    </button>

    <!-- 제목 -->
    <span class="flex-1 {{ 'line-through text-gray-400' if todo.is_completed
                          else 'text-gray-900 dark:text-white' }}">
        {{ todo.title }}
    </span>

    <!-- 삭제 버튼 -->
    <!--
    hx-delete: DELETE 요청
    hx-swap="delete": 응답 후 이 요소 삭제
    hx-confirm: 삭제 전 확인 대화상자
    -->
    <button hx-delete="/partials/todos/{{ todo.id }}"
            hx-swap="delete"
            hx-target="#todo-{{ todo.id }}"
            hx-confirm="정말 삭제하시겠습니까?"
            class="text-gray-400 hover:text-red-500 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
    </button>
</div>
```

### 7.3 목록 파셜 템플릿

`templates/partials/todos/list.html`:

```html
<!--
Todo 목록 파셜

전체 목록을 갱신할 때 사용됩니다.
-->
{% for todo in todos %}
    {% include "partials/todos/item.html" %}
{% else %}
    <p class="text-center text-gray-500 py-8">
        할 일이 없습니다.
    </p>
{% endfor %}
```

---

## Step 8: 라우터 등록

### API 라우터 등록

`app/api/v1/router.py`에 추가:

```python
from app.api.v1.todos import router as todos_router

# 기존 라우터들 아래에 추가
api_router.include_router(todos_router)
```

### 페이지 라우터 등록

`app/pages/router.py`에 추가:

```python
from app.pages.todos import router as todos_router

# 기존 라우터들 아래에 추가
pages_router.include_router(todos_router)
```

### 파셜 라우터 등록

`app/partials/router.py`에 추가:

```python
from app.partials.todos import router as todos_router

# 기존 라우터들 아래에 추가
partials_router.include_router(todos_router)
```

---

## Step 9: 테스트

### 데이터베이스 마이그레이션

```bash
# Alembic으로 마이그레이션 생성
alembic revision --autogenerate -m "Add todos table"

# 마이그레이션 적용
alembic upgrade head
```

### 서버 실행

```bash
uvicorn app.main:app --reload
```

### 테스트

1. 브라우저에서 `http://localhost:8000/login`으로 로그인
2. `http://localhost:8000/todos`로 이동
3. 새 할 일 추가, 완료 토글, 삭제 테스트

### API 테스트 (선택)

```bash
# Todo 생성
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Cookie: access_token=YOUR_TOKEN" \
  -d '{"title": "테스트 할 일"}'

# Todo 목록 조회
curl http://localhost:8000/api/v1/todos \
  -H "Cookie: access_token=YOUR_TOKEN"
```

---

## 완성된 코드 요약

### 파일 목록

| 파일 | 역할 |
|------|------|
| `app/models/todo.py` | DB 테이블 정의 |
| `app/schemas/todo.py` | 데이터 검증 |
| `app/services/todo.py` | 비즈니스 로직 |
| `app/api/v1/todos.py` | REST API |
| `app/pages/todos.py` | 페이지 렌더링 |
| `app/partials/todos.py` | HTMX 파셜 |
| `templates/pages/todos.html` | 메인 페이지 |
| `templates/partials/todos/item.html` | 아이템 파셜 |
| `templates/partials/todos/list.html` | 목록 파셜 |

### 데이터 흐름

```
사용자 액션
    ↓
HTMX 속성 (hx-post, hx-get 등)
    ↓
Partial Router (app/partials/todos.py)
    ↓
Service Layer (app/services/todo.py)
    ↓
Database Model (app/models/todo.py)
    ↓
Template (templates/partials/todos/*.html)
    ↓
DOM 업데이트 (hx-swap)
```

---

## 다음 단계

이 튜토리얼을 완료했다면 다음을 시도해보세요:

1. **검색 기능 추가**: `hx-trigger="keyup changed delay:300ms"` 사용
2. **드래그앤드롭 정렬**: Sortable.js와 HTMX 연동
3. **카테고리 기능**: Todo에 카테고리 필드 추가
4. **우선순위 기능**: 중요도에 따른 정렬
5. **마감일 기능**: 날짜 필드와 알림

축하합니다! 🎉 첫 번째 CRUD 기능을 완성했습니다!
