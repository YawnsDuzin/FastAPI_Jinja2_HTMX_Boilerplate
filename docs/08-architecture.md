# 아키텍처 설명

이 문서는 FastAPI + Jinja2 + HTMX 보일러플레이트의 전체 아키텍처와 각 구성 요소의 역할을 상세히 설명합니다.

## 1. 전체 아키텍처 개요

### 1.1 시스템 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Client (Browser)                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │   HTML   │  │   HTMX   │  │ Alpine.js│  │Tailwind  │  │  Cookies  │ │
│  │ (렌더링) │  │(AJAX요청)│  │(UI상태)  │  │ (스타일) │  │ (JWT토큰) │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/HTTPS
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Application                              │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                        Middleware Layer                              │ │
│ │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│ │  │   CORS   │  │ Session  │  │Exception │  │  Gzip    │            │ │
│ │  │Middleware│  │Middleware│  │ Handler  │  │Middleware│            │ │
│ │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                         Router Layer                                 │ │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │ │
│ │  │   API v1     │  │    Pages     │  │   Partials   │              │ │
│ │  │ /api/v1/*    │  │     /*       │  │ /partials/*  │              │ │
│ │  │ (JSON응답)   │  │ (전체HTML)   │  │ (HTML조각)   │              │ │
│ │  └──────────────┘  └──────────────┘  └──────────────┘              │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                      Dependencies Layer                              │ │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │ │
│ │  │ CurrentUser  │  │  DbSession   │  │   Services   │              │ │
│ │  │ (인증의존성) │  │ (DB세션)     │  │ (비즈니스)   │              │ │
│ │  └──────────────┘  └──────────────┘  └──────────────┘              │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                        Service Layer                                 │ │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │ │
│ │  │ AuthService  │  │ UserService  │  │ ItemService  │              │ │
│ │  │ (인증로직)   │  │ (사용자CRUD) │  │ (아이템CRUD) │              │ │
│ │  └──────────────┘  └──────────────┘  └──────────────┘              │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                         Model Layer                                  │ │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │ │
│ │  │SQLAlchemy ORM│  │   Pydantic   │  │   Alembic    │              │ │
│ │  │ (DB모델)     │  │ (스키마검증) │  │ (마이그레이션)│              │ │
│ │  └──────────────┘  └──────────────┘  └──────────────┘              │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Async I/O
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Database Layer                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │         SQLite (개발) / PostgreSQL (프로덕션) / MySQL            │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 핵심 설계 원칙

| 원칙 | 설명 | 구현 방법 |
|------|------|----------|
| **관심사의 분리** | 각 계층이 단일 책임을 가짐 | Router/Service/Model 분리 |
| **의존성 역전** | 상위 계층이 하위 계층에 의존하지 않음 | FastAPI Depends() 활용 |
| **비동기 처리** | I/O 작업의 논블로킹 처리 | async/await 패턴 |
| **타입 안전성** | 런타임 + 정적 타입 검사 | Pydantic + mypy |

## 2. 3가지 라우터 레이어 상세

이 보일러플레이트의 핵심은 **용도에 따른 3가지 라우터 분리**입니다.

### 2.1 라우터 비교표

| 레이어 | 경로 패턴 | 응답 타입 | 주요 용도 | 클라이언트 |
|--------|----------|----------|----------|-----------|
| **API** | `/api/v1/*` | JSON | 외부 연동, 모바일 앱 | fetch, axios |
| **Pages** | `/*` | 전체 HTML | 첫 페이지 로드, SEO | 브라우저 직접 |
| **Partials** | `/partials/*` | HTML 조각 | HTMX 부분 업데이트 | HTMX |

### 2.2 API 레이어 (app/api/v1/)

**목적**: REST API 제공, JSON 응답

```python
# app/api/v1/items.py - API 예시

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import CurrentUser, DbSession
from app.schemas.item import ItemCreate, ItemResponse, ItemListResponse
from app.services.item import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=ItemListResponse)
async def get_items(
    db: DbSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> ItemListResponse:
    """
    아이템 목록 조회 API

    - JSON 응답 반환
    - Pydantic 모델로 자동 직렬화
    - OpenAPI 문서 자동 생성
    """
    service = ItemService(db)
    items = await service.get_multi(owner_id=current_user.id, skip=skip, limit=limit)
    total = await service.count(owner_id=current_user.id)

    return ItemListResponse(items=items, total=total)

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,  # Pydantic이 자동 검증
    db: DbSession,
    current_user: CurrentUser,
) -> ItemResponse:
    """아이템 생성 API"""
    service = ItemService(db)
    item = await service.create(item_in, owner_id=current_user.id)
    return item
```

**API 레이어 특징**:
- 순수한 JSON 응답
- Swagger UI 자동 문서화 (`/docs`)
- 외부 클라이언트(모바일 앱, 다른 서비스) 연동용
- 버전 관리 가능 (`/api/v1/`, `/api/v2/`)

### 2.3 Pages 레이어 (app/pages/)

**목적**: 완전한 HTML 페이지 제공 (SSR)

```python
# app/pages/items.py - Pages 예시

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.api.deps import CurrentUser, DbSession
from app.core.templating import templates
from app.services.item import ItemService

router = APIRouter(tags=["pages"])

@router.get("/items", response_class=HTMLResponse)
async def items_page(
    request: Request,
    db: DbSession,
    current_user: CurrentUser,
):
    """
    아이템 목록 페이지

    - base.html을 상속하는 전체 HTML 반환
    - 네비게이션, 푸터 포함
    - SEO 친화적 (검색엔진이 인덱싱 가능)
    """
    service = ItemService(db)
    items = await service.get_multi(owner_id=current_user.id)

    return templates.TemplateResponse(
        "pages/items/index.html",
        {
            "request": request,
            "items": items,
            "user": current_user,
            "page_title": "내 아이템",
        }
    )
```

**Pages 레이어 특징**:
- `base.html` 상속으로 전체 레이아웃 포함
- 브라우저 직접 접속 또는 링크 클릭 시 사용
- SEO를 위한 메타 태그, 구조화된 데이터 포함 가능
- 첫 페이지 로드 시 완전한 HTML 제공

### 2.4 Partials 레이어 (app/partials/)

**목적**: HTMX용 HTML 조각 제공

```python
# app/partials/items.py - Partials 예시

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from app.api.deps import CurrentUser, DbSession
from app.core.templating import templates
from app.services.item import ItemService

router = APIRouter(prefix="/partials/items", tags=["partials"])

@router.get("", response_class=HTMLResponse)
async def items_list_partial(
    request: Request,
    db: DbSession,
    current_user: CurrentUser,
):
    """
    아이템 목록 파셜

    - HTML 조각만 반환 (base.html 없음)
    - HTMX hx-target에 삽입됨
    - 페이지 새로고침 없이 부분 업데이트
    """
    service = ItemService(db)
    items = await service.get_multi(owner_id=current_user.id)

    return templates.TemplateResponse(
        "partials/items/list.html",  # 목록만 있는 템플릿
        {"request": request, "items": items}
    )

@router.post("", response_class=HTMLResponse)
async def create_item_partial(
    request: Request,
    db: DbSession,
    current_user: CurrentUser,
    title: str = Form(...),
    description: str = Form(None),
):
    """아이템 생성 후 목록 반환"""
    service = ItemService(db)
    await service.create(
        ItemCreate(title=title, description=description),
        owner_id=current_user.id
    )

    # 생성 후 업데이트된 목록 반환
    items = await service.get_multi(owner_id=current_user.id)

    response = templates.TemplateResponse(
        "partials/items/list.html",
        {"request": request, "items": items}
    )
    # HTMX 이벤트 트리거 (토스트 알림)
    response.headers["HX-Trigger"] = '{"showToast": {"message": "아이템이 생성되었습니다", "type": "success"}}'

    return response
```

**Partials 레이어 특징**:
- `base.html` 상속 없음, 순수 HTML 조각
- HTMX의 `hx-target`에 삽입될 컨텐츠
- 빠른 응답 (필요한 부분만 렌더링)
- `HX-Trigger` 헤더로 클라이언트 이벤트 발생

### 2.5 3가지 레이어의 협력

```
┌─────────────────────────────────────────────────────────────────┐
│                         요청 흐름 예시                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 첫 접속: GET /items                                         │
│     └─ Pages Layer → 전체 HTML (네비게이션 + 컨텐츠 + 푸터)      │
│                                                                 │
│  2. 새로고침 버튼 클릭: GET /partials/items (HTMX)               │
│     └─ Partials Layer → 아이템 목록 HTML만                       │
│     └─ HTMX가 #item-list에 삽입                                 │
│                                                                 │
│  3. 외부 앱 요청: GET /api/v1/items                             │
│     └─ API Layer → JSON 데이터                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 3. 요청 처리 흐름 상세

### 3.1 일반적인 페이지 요청

```
┌─────────────────────────────────────────────────────────────────┐
│                    페이지 요청 흐름                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  브라우저 ─── GET /dashboard ───▶ FastAPI                       │
│                                     │                           │
│                              ┌──────▼──────┐                    │
│                              │ Middleware  │                    │
│                              │ - CORS 검사 │                    │
│                              │ - 세션 처리 │                    │
│                              └──────┬──────┘                    │
│                                     │                           │
│                              ┌──────▼──────┐                    │
│                              │Pages Router │                    │
│                              │dashboard.py │                    │
│                              └──────┬──────┘                    │
│                                     │                           │
│                              ┌──────▼──────┐                    │
│                              │Dependencies │                    │
│                              │- DbSession  │                    │
│                              │- CurrentUser│                    │
│                              └──────┬──────┘                    │
│                                     │                           │
│                              ┌──────▼──────┐                    │
│                              │Service Layer│                    │
│                              │ 비즈니스로직│                    │
│                              └──────┬──────┘                    │
│                                     │                           │
│                              ┌──────▼──────┐                    │
│                              │  Database   │                    │
│                              │   조회      │                    │
│                              └──────┬──────┘                    │
│                                     │                           │
│                              ┌──────▼──────┐                    │
│                              │  Jinja2     │                    │
│                              │ 템플릿렌더링│                    │
│                              └──────┬──────┘                    │
│                                     │                           │
│  브라우저 ◀── 전체 HTML 페이지 ───┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 HTMX 파셜 요청

```
┌─────────────────────────────────────────────────────────────────┐
│                    HTMX 파셜 요청 흐름                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  사용자가 버튼 클릭                                              │
│  <button hx-get="/partials/items" hx-target="#list">            │
│         │                                                       │
│         ▼                                                       │
│  HTMX가 자동으로 AJAX 요청 생성                                  │
│  - Headers: HX-Request: true                                    │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐                                          │
│  │ Partials Router  │                                          │
│  │ items.py         │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐                                          │
│  │ Service Layer    │                                          │
│  │ DB 조회          │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐                                          │
│  │ Jinja2 렌더링    │                                          │
│  │ (파셜 템플릿만)  │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│           ▼                                                     │
│  HTML 조각 응답 + HX-Trigger 헤더                               │
│         │                                                       │
│         ▼                                                       │
│  HTMX가 #list 요소의 내용을 교체                                 │
│  + HX-Trigger 이벤트 처리 (토스트 등)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 API 요청

```
┌─────────────────────────────────────────────────────────────────┐
│                      API 요청 흐름                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  클라이언트 (모바일 앱, 외부 서비스, fetch)                      │
│  POST /api/v1/items                                             │
│  Content-Type: application/json                                 │
│  Cookie: access_token=xxx                                       │
│  Body: {"title": "새 아이템", "description": "설명"}            │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐                                          │
│  │ Pydantic 검증    │                                          │
│  │ ItemCreate 스키마│                                          │
│  └────────┬─────────┘                                          │
│           │ 검증 실패 시 → 422 Unprocessable Entity             │
│           ▼                                                     │
│  ┌──────────────────┐                                          │
│  │ 인증 의존성      │                                          │
│  │ CurrentUser      │                                          │
│  └────────┬─────────┘                                          │
│           │ 인증 실패 시 → 401 Unauthorized                     │
│           ▼                                                     │
│  ┌──────────────────┐                                          │
│  │ Service Layer    │                                          │
│  │ ItemService      │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐                                          │
│  │ Database 저장    │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│           ▼                                                     │
│  JSON 응답 (Pydantic 직렬화)                                    │
│  {"id": 1, "title": "새 아이템", "created_at": "..."}           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 4. 계층별 상세 설명

### 4.1 Router Layer (라우터 계층)

```
app/
├── api/
│   ├── __init__.py
│   ├── deps.py              # 의존성 정의
│   └── v1/
│       ├── __init__.py
│       ├── auth.py          # 인증 API
│       ├── users.py         # 사용자 API
│       └── items.py         # 아이템 API
├── pages/
│   ├── __init__.py
│   ├── home.py              # 홈페이지
│   ├── auth.py              # 로그인/회원가입 페이지
│   ├── dashboard.py         # 대시보드 페이지
│   └── items.py             # 아이템 페이지
└── partials/
    ├── __init__.py
    ├── items.py             # 아이템 파셜
    ├── modals.py            # 모달 파셜
    └── toasts.py            # 토스트 파셜
```

**라우터의 책임**:
| 책임 | 설명 |
|------|------|
| HTTP 처리 | 요청 수신, 응답 반환 |
| 입력 검증 | Pydantic 스키마로 요청 데이터 검증 |
| 의존성 주입 | `Depends()`로 필요한 서비스/DB 세션 주입 |
| 응답 형식 | JSON 또는 HTML 선택 |

### 4.2 Dependencies Layer (의존성 계층)

```python
# app/api/deps.py

from typing import Annotated
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User

# 데이터베이스 세션 의존성
async def get_db_session() -> AsyncSession:
    async with get_db() as session:
        yield session

DbSession = Annotated[AsyncSession, Depends(get_db_session)]

# 현재 사용자 의존성 (필수)
async def get_current_user(
    db: DbSession,
    access_token: str | None = Cookie(default=None),
) -> User:
    """
    JWT 토큰에서 현재 사용자 추출
    - 토큰 없음 → 401 Unauthorized
    - 토큰 만료 → 401 Unauthorized
    - 사용자 없음 → 401 Unauthorized
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다",
        )

    payload = verify_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다",
        )

    user = await db.get(User, payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
        )

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

# 현재 사용자 의존성 (선택)
async def get_current_user_optional(
    db: DbSession,
    access_token: str | None = Cookie(default=None),
) -> User | None:
    """인증 선택적 - 토큰 없어도 None 반환"""
    if not access_token:
        return None

    try:
        return await get_current_user(db, access_token)
    except HTTPException:
        return None

CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
```

### 4.3 Service Layer (서비스 계층)

```python
# app/services/item.py

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    """
    아이템 비즈니스 로직

    - CRUD 작업 수행
    - 비즈니스 규칙 적용
    - 트랜잭션 관리는 호출자에게 위임
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, item_id: int) -> Item | None:
        """단일 아이템 조회"""
        return await self.db.get(Item, item_id)

    async def get_multi(
        self,
        owner_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Item]:
        """아이템 목록 조회 (페이지네이션)"""
        stmt = (
            select(Item)
            .where(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(self, owner_id: int) -> int:
        """아이템 개수 조회"""
        stmt = select(func.count()).select_from(Item).where(Item.owner_id == owner_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def create(self, item_in: ItemCreate, owner_id: int) -> Item:
        """아이템 생성"""
        item = Item(
            title=item_in.title,
            description=item_in.description,
            owner_id=owner_id,
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, item_in: ItemUpdate) -> Item:
        """아이템 수정"""
        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        """아이템 삭제"""
        await self.db.delete(item)
        await self.db.commit()
```

**서비스 계층의 책임**:
| 책임 | 설명 |
|------|------|
| 비즈니스 로직 | 도메인 규칙 구현 |
| 데이터 조작 | CRUD 작업 수행 |
| 예외 발생 | 비즈니스 규칙 위반 시 예외 |
| 트랜잭션 | commit/rollback 관리 |

### 4.4 Model Layer (모델 계층)

```python
# app/models/item.py

from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Item(Base):
    """
    아이템 모델

    SQLAlchemy 2.0 스타일의 선언적 매핑 사용
    """
    __tablename__ = "items"

    # 기본 키
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # 필드
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    # 외래 키 (소유자)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    # 관계
    owner: Mapped["User"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title='{self.title}')>"
```

### 4.5 Schema Layer (스키마 계층)

```python
# app/schemas/item.py

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ItemBase(BaseModel):
    """아이템 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=200, description="아이템 제목")
    description: str | None = Field(None, max_length=5000, description="아이템 설명")

class ItemCreate(ItemBase):
    """아이템 생성 스키마"""
    pass

class ItemUpdate(BaseModel):
    """아이템 수정 스키마 (모든 필드 선택적)"""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=5000)
    is_active: bool | None = None

class ItemResponse(ItemBase):
    """아이템 응답 스키마"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime | None

class ItemListResponse(BaseModel):
    """아이템 목록 응답 스키마"""
    items: list[ItemResponse]
    total: int
```

**Model vs Schema 비교**:
| 구분 | Model (SQLAlchemy) | Schema (Pydantic) |
|------|-------------------|-------------------|
| 용도 | 데이터베이스 테이블 정의 | API 요청/응답 데이터 정의 |
| 검증 | DB 제약 조건 | 런타임 데이터 검증 |
| 변환 | ORM 객체 ↔ DB | Python 객체 ↔ JSON |
| 관계 | relationship() 지원 | 중첩 모델로 표현 |

## 5. 인증 아키텍처

### 5.1 JWT 인증 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                       JWT 인증 흐름                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 로그인                                                       │
│  ┌─────────┐    POST /api/v1/auth/login    ┌─────────────────┐ │
│  │ Client  │ ─────────────────────────────▶│   AuthService   │ │
│  │         │    {email, password}          │                 │ │
│  │         │                               │  - 사용자 조회  │ │
│  │         │                               │  - 비밀번호 검증│ │
│  │         │                               │  - JWT 생성     │ │
│  │         │◀───────────────────────────── │                 │ │
│  │         │    Set-Cookie: access_token   └─────────────────┘ │
│  └─────────┘                                                    │
│                                                                 │
│  2. 인증된 요청                                                  │
│  ┌─────────┐    GET /dashboard             ┌─────────────────┐ │
│  │ Client  │ ─────────────────────────────▶│ get_current_user│ │
│  │         │    Cookie: access_token=xxx   │                 │ │
│  │         │                               │  - 토큰 추출    │ │
│  │         │                               │  - 토큰 검증    │ │
│  │         │                               │  - 사용자 조회  │ │
│  │         │◀───────────────────────────── │  - User 반환    │ │
│  │         │    HTML 페이지                └─────────────────┘ │
│  └─────────┘                                                    │
│                                                                 │
│  3. 로그아웃                                                     │
│  ┌─────────┐    POST /api/v1/auth/logout   ┌─────────────────┐ │
│  │ Client  │ ─────────────────────────────▶│   AuthService   │ │
│  │         │                               │                 │ │
│  │         │◀───────────────────────────── │  - 쿠키 삭제    │ │
│  │         │    Set-Cookie: access_token=  └─────────────────┘ │
│  │         │    (빈 값, 만료)                                   │
│  └─────────┘                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 토큰 저장 방식 비교

| 방식 | 장점 | 단점 | 이 프로젝트 |
|------|------|------|------------|
| **httpOnly Cookie** | XSS 공격에 안전 | CSRF 주의 필요 | ✅ 사용 |
| localStorage | 간편한 접근 | XSS 취약 | ❌ |
| sessionStorage | 탭 단위 격리 | XSS 취약 | ❌ |

### 5.3 보안 설정

```python
# app/core/security.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int) -> str:
    """JWT 액세스 토큰 생성"""
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict | None:
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
```

## 6. 템플릿 렌더링 아키텍처

### 6.1 템플릿 상속 구조

```
templates/
├── base.html                 # 최상위 레이아웃
│   ├── <head> (CSS, 메타태그)
│   ├── <body>
│   │   ├── {% include "components/navbar.html" %}
│   │   ├── {% block content %}{% endblock %}
│   │   └── {% include "components/footer.html" %}
│   └── <script> (JS, HTMX, Alpine)
│
├── pages/
│   └── items/
│       └── index.html        # {% extends "base.html" %}
│           └── {% block content %}
│               └── 페이지 컨텐츠
│               └── {% include "partials/items/list.html" %}
│
└── partials/
    └── items/
        └── list.html         # base 상속 없음, 순수 HTML
```

### 6.2 템플릿 렌더링 다이어그램

```
┌──────────────────────────────────────────────────────────────────┐
│                        base.html                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     <head>                                  │ │
│  │  - TailwindCSS                                             │ │
│  │  - Alpine.js                                               │ │
│  │  - HTMX                                                    │ │
│  │  - 커스텀 CSS                                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              navbar.html (include)                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              {% block content %}                            │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │                pages/items/index.html                 │ │ │
│  │  │  (extends base.html)                                  │ │ │
│  │  │                                                       │ │ │
│  │  │  ┌────────────────────────────────────────────────┐ │ │ │
│  │  │  │         <div id="item-list">                   │ │ │ │
│  │  │  │           HTMX Target                          │ │ │ │
│  │  │  │  ┌──────────────────────────────────────────┐ │ │ │ │
│  │  │  │  │    partials/items/list.html (include)    │ │ │ │ │
│  │  │  │  │    - 순수 HTML 조각                      │ │ │ │ │
│  │  │  │  │    - HTMX로 교체 가능                    │ │ │ │ │
│  │  │  │  └──────────────────────────────────────────┘ │ │ │ │
│  │  │  └────────────────────────────────────────────────┘ │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              footer.html (include)                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              toast.html (include)                           │ │
│  │              - Alpine.js 상태 관리                          │ │
│  │              - HX-Trigger로 표시                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## 7. 에러 처리 아키텍처

### 7.1 예외 계층 구조

```python
# app/core/exceptions.py

from fastapi import HTTPException, status

class AppException(HTTPException):
    """애플리케이션 기본 예외"""
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "서버 오류가 발생했습니다",
    ):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(AppException):
    """리소스를 찾을 수 없음"""
    def __init__(self, resource: str = "리소스"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource}를 찾을 수 없습니다",
        )

class UnauthorizedError(AppException):
    """인증 실패"""
    def __init__(self, detail: str = "인증이 필요합니다"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

class ForbiddenError(AppException):
    """권한 없음"""
    def __init__(self, detail: str = "권한이 없습니다"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

class ValidationError(AppException):
    """검증 오류"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )
```

### 7.2 에러 응답 형식

```
┌─────────────────────────────────────────────────────────────────┐
│                      에러 응답 처리                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API 요청 에러:                                                 │
│  ──────────────                                                 │
│  HTTP 401 Unauthorized                                          │
│  Content-Type: application/json                                 │
│  {                                                              │
│    "detail": "인증이 필요합니다"                                │
│  }                                                              │
│                                                                 │
│  HTMX 요청 에러:                                                │
│  ────────────────                                               │
│  HTTP 401 Unauthorized                                          │
│  HX-Trigger: {"showToast": {"message": "인증이 필요합니다",     │
│                              "type": "error"}}                  │
│  또는 로그인 페이지로 리다이렉트                                │
│  HX-Redirect: /login                                           │
│                                                                 │
│  Pages 요청 에러:                                               │
│  ────────────────                                               │
│  HTTP 302 Redirect → /login?next=/dashboard                    │
│  또는 에러 페이지 렌더링                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 8. 확장 가이드

### 8.1 새 기능 추가 체크리스트

```
새 기능: "댓글" 추가 예시
─────────────────────────

□ 1. 모델 생성
   파일: app/models/comment.py
   - Comment 클래스 정의
   - 관계 설정 (User, Item)

□ 2. 마이그레이션 생성/적용
   명령: alembic revision --autogenerate -m "add comments"
   명령: alembic upgrade head

□ 3. 스키마 생성
   파일: app/schemas/comment.py
   - CommentCreate
   - CommentUpdate
   - CommentResponse

□ 4. 서비스 생성
   파일: app/services/comment.py
   - CommentService 클래스
   - CRUD 메서드

□ 5. API 라우터 추가
   파일: app/api/v1/comments.py
   - GET, POST, PATCH, DELETE 엔드포인트
   등록: app/api/v1/__init__.py

□ 6. 파셜 라우터 추가
   파일: app/partials/comments.py
   - 댓글 목록 파셜
   - 댓글 추가 파셜
   등록: app/partials/__init__.py

□ 7. 템플릿 생성
   폴더: templates/partials/comments/
   - list.html (목록)
   - form.html (입력 폼)
   - item.html (단일 댓글)

□ 8. 기존 템플릿 수정
   파일: templates/pages/items/detail.html
   - 댓글 섹션 추가

□ 9. 테스트 작성
   파일: tests/test_api/test_comments.py
   파일: tests/test_services/test_comment.py
```

### 8.2 디렉토리 구조 확장

```
app/
├── models/
│   ├── __init__.py          # 모든 모델 export
│   ├── base.py
│   ├── user.py
│   ├── item.py
│   └── comment.py           # 새 모델
│
├── schemas/
│   ├── __init__.py
│   ├── common.py
│   ├── user.py
│   ├── item.py
│   └── comment.py           # 새 스키마
│
├── services/
│   ├── __init__.py
│   ├── auth.py
│   ├── user.py
│   ├── item.py
│   └── comment.py           # 새 서비스
│
├── api/v1/
│   ├── __init__.py          # 라우터 등록
│   ├── auth.py
│   ├── users.py
│   ├── items.py
│   └── comments.py          # 새 API
│
├── partials/
│   ├── __init__.py
│   ├── items.py
│   └── comments.py          # 새 파셜
│
└── pages/
    ├── __init__.py
    └── items.py             # 기존 수정
```

## 9. 성능 고려사항

### 9.1 비동기 처리 장점

```
┌─────────────────────────────────────────────────────────────────┐
│                    동기 vs 비동기 처리                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  동기 처리 (Flask 등):                                          │
│  ────────────────────                                           │
│  요청1 ████████████████░░░░░░░░░░░░░░░░░░░░░░░ (DB 대기)        │
│  요청2 ░░░░░░░░░░░░░░░░████████████████░░░░░░░ (차례 대기)      │
│  요청3 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████                 │
│                                                                 │
│  비동기 처리 (FastAPI):                                         │
│  ─────────────────────                                          │
│  요청1 ████▓▓▓▓▓▓▓▓▓▓▓▓████ (DB 대기 중 다른 요청 처리)         │
│  요청2 ░░░░████▓▓▓▓▓▓▓▓████                                     │
│  요청3 ░░░░░░░░████▓▓▓▓████                                     │
│                                                                 │
│  ████ = CPU 작업 (코드 실행)                                    │
│  ▓▓▓▓ = I/O 대기 (DB, 네트워크)                                │
│  ░░░░ = 대기                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 최적화 포인트

| 영역 | 최적화 방법 | 구현 |
|------|------------|------|
| **DB 쿼리** | 필요한 컬럼만 조회 | `select(Item.id, Item.title)` |
| **페이지네이션** | offset/limit 사용 | `skip`, `limit` 파라미터 |
| **캐싱** | Redis 캐시 | 자주 조회되는 데이터 캐싱 |
| **N+1 문제** | joinedload | `options(joinedload(Item.owner))` |
| **템플릿** | Jinja2 캐싱 | 자동 (프로덕션 모드) |

## 10. 다음 단계

- 📁 [디렉토리 구조](./09-directory-structure.md) - 파일별 상세 설명
- 🔧 [개발 환경 설정](./10-development-setup.md) - 에디터, 도구 설정
- 🧪 [테스트 가이드](./11-testing-guide.md) - 테스트 작성법
- 🚀 [배포 가이드](./12-deployment-guide.md) - 프로덕션 배포
