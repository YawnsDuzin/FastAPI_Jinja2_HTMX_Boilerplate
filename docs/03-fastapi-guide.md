# FastAPI 가이드

## 1. FastAPI 소개

FastAPI는 Python 3.7+로 API를 구축하기 위한 현대적이고 빠른 웹 프레임워크입니다.

### 주요 특징
- **빠른 성능**: Starlette + Pydantic 기반
- **자동 문서화**: OpenAPI(Swagger) 자동 생성
- **타입 검증**: Python 타입 힌트로 자동 검증
- **비동기 지원**: async/await 네이티브 지원

## 2. 기본 문법

### 2.1 라우터 정의

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter()

# GET 요청
@router.get("/items")
async def get_items():
    return {"items": []}

# POST 요청
@router.post("/items")
async def create_item(item: ItemCreate):
    return item

# 경로 매개변수
@router.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# 쿼리 매개변수
@router.get("/search")
async def search(q: str, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}
```

### 2.2 요청 데이터

```python
from pydantic import BaseModel, Field
from typing import Optional

# Pydantic 모델로 요청 바디 정의
class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(default=0, ge=0, le=10)

# 요청 바디 사용
@router.post("/items")
async def create_item(item: ItemCreate):
    return item

# Form 데이터
from fastapi import Form

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

### 2.3 응답 정의

```python
from fastapi.responses import JSONResponse, HTMLResponse

# 응답 모델 지정
@router.get("/items/{id}", response_model=Item)
async def get_item(id: int):
    return Item(id=id, title="Test")

# HTML 응답
@router.get("/page", response_class=HTMLResponse)
async def get_page():
    return "<html><body>Hello</body></html>"

# 상태 코드 지정
@router.post("/items", status_code=201)
async def create_item(item: ItemCreate):
    return item

# 커스텀 헤더
@router.get("/custom")
async def custom_response():
    response = JSONResponse(content={"message": "Hello"})
    response.headers["X-Custom-Header"] = "Value"
    return response
```

### 2.4 의존성 주입

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 의존성 함수
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# 의존성 사용
@router.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    # db 세션 사용
    pass

# 타입 어노테이션으로 의존성
from typing import Annotated

DbSession = Annotated[AsyncSession, Depends(get_db)]

@router.get("/items")
async def get_items(db: DbSession):
    pass
```

### 2.5 에러 처리

```python
from fastapi import HTTPException

# HTTPException 발생
@router.get("/items/{id}")
async def get_item(id: int):
    if id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": id}

# 커스텀 예외
class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

# 예외 핸들러
@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": exc.message}
    )
```

## 3. 이 프로젝트의 FastAPI 패턴

### 3.1 라우터 구조

```
app/
├── api/                    # REST API
│   └── v1/
│       ├── router.py      # 라우터 통합
│       ├── auth.py        # 인증 API
│       ├── items.py       # 아이템 API
│       └── users.py       # 사용자 API
├── pages/                  # HTML 페이지
│   ├── router.py
│   ├── home.py
│   ├── auth.py
│   └── dashboard.py
└── partials/              # HTMX 파셜
    ├── router.py
    ├── items.py
    ├── modals.py
    └── toasts.py
```

### 3.2 페이지 라우터 (HTML 응답)

```python
# app/pages/home.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/home.html",
        context={"title": "홈"}
    )
```

### 3.3 파셜 라우터 (HTMX 응답)

```python
# app/partials/items.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("", response_class=HTMLResponse)
async def get_items_partial(request: Request):
    items = await item_service.get_all()
    return templates.TemplateResponse(
        request=request,
        name="partials/items/list.html",
        context={"items": items}
    )

@router.delete("/{item_id}", response_class=HTMLResponse)
async def delete_item(item_id: int):
    await item_service.delete(item_id)
    response = HTMLResponse(content="")
    response.headers["HX-Trigger"] = "showToast"
    return response
```

### 3.4 서비스 레이어

```python
# app/services/item.py
class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, owner_id: int) -> list[Item]:
        query = select(Item).where(Item.owner_id == owner_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, item_in: ItemCreate, owner: User) -> Item:
        item = Item(**item_in.model_dump(), owner_id=owner.id)
        self.db.add(item)
        await self.db.flush()
        return item
```

### 3.5 의존성 정의

```python
# app/api/deps.py
from typing import Annotated
from fastapi import Depends

# 현재 사용자
async def get_current_user(
    db: DbSession,
    token: str = Depends(get_token_from_cookie),
) -> User:
    # 토큰 검증 및 사용자 반환
    pass

CurrentUser = Annotated[User, Depends(get_current_user)]

# 라우터에서 사용
@router.get("/items")
async def get_items(current_user: CurrentUser):
    pass
```

## 4. 비동기 프로그래밍

### 4.1 async/await 기본

```python
import asyncio

# 비동기 함수
async def fetch_data():
    await asyncio.sleep(1)
    return "data"

# 여러 작업 동시 실행
async def fetch_all():
    task1 = fetch_data()
    task2 = fetch_data()
    results = await asyncio.gather(task1, task2)
    return results
```

### 4.2 비동기 데이터베이스

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_users(db: AsyncSession):
    query = select(User).where(User.is_active == True)
    result = await db.execute(query)
    return result.scalars().all()
```

## 5. 테스트

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    response = await client.get("/api/v1/items")
    assert response.status_code == 200
```

## 6. 유용한 팁

### 6.1 백그라운드 작업

```python
from fastapi import BackgroundTasks

@router.post("/send-email")
async def send_email(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email_task, email)
    return {"message": "이메일 전송 예약됨"}
```

### 6.2 미들웨어

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        import time
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Process-Time"] = str(duration)
        return response

app.add_middleware(TimingMiddleware)
```

### 6.3 라이프사이클 이벤트

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    await init_db()
    yield
    # 종료 시 실행
    await close_db()

app = FastAPI(lifespan=lifespan)
```

## 7. 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com)
- [Starlette 문서](https://www.starlette.io)
- [Pydantic 문서](https://docs.pydantic.dev)
