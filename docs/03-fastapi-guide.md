# FastAPI 가이드

## 1. FastAPI란 무엇인가?

### 1.1 기본 개념

FastAPI는 Python으로 웹 API를 만들 수 있는 프레임워크입니다. 일반 Python만 사용해보셨다면, 웹 프레임워크가 생소할 수 있습니다.

**웹 프레임워크란?**
- 웹 브라우저나 앱에서 오는 요청(Request)을 받아서
- 그에 맞는 처리를 하고
- 응답(Response)을 돌려주는 프로그램을 쉽게 만들게 해주는 도구입니다

**예를 들어:**
```
사용자 → 웹 브라우저에서 "example.com/users" 접속
         ↓
FastAPI → "/users" 주소로 요청이 왔네? 사용자 목록을 보여줘야지!
         ↓
사용자 → 사용자 목록 화면을 봄
```

### 1.2 왜 FastAPI인가?

| 특징 | 설명 | 일반 Python과의 차이 |
|------|------|---------------------|
| 자동 문서화 | API 문서가 자동으로 생성됨 | 따로 문서 안 써도 됨 |
| 타입 검증 | 잘못된 데이터가 오면 자동으로 에러 | if문으로 일일이 검사 안 해도 됨 |
| 비동기 지원 | 여러 요청을 동시에 처리 가능 | 순차적으로만 처리되던 것이 병렬 처리 가능 |
| 빠른 속도 | Node.js, Go와 비슷한 성능 | 일반 Python보다 훨씬 빠름 |

---

## 2. 기본 개념 이해하기

### 2.1 라우터(Router)란?

라우터는 **"어떤 주소로 요청이 오면 어떤 함수를 실행할지"** 를 정의합니다.

```python
# ============================================================
# 라우터 생성 - 관련 기능들을 묶어주는 그룹
# ============================================================
from fastapi import APIRouter  # FastAPI에서 라우터 기능을 가져옴

router = APIRouter()  # 새 라우터 객체 생성
# → 이 router에 여러 경로(주소)들을 등록할 수 있음

# ============================================================
# 데코레이터(@)로 경로 등록하기
# ============================================================
@router.get("/items")  # GET 방식으로 "/items" 주소에 접근하면
async def get_items():  # 이 함수가 실행됨
    return {"items": []}  # 이 데이터를 응답으로 보냄
```

**데코레이터(@) 설명:**
```python
@router.get("/items")
# ↑ 이것을 '데코레이터'라고 부름
# 의미: "아래 함수를 GET /items 요청이 올 때 실행해라"

# 데코레이터 없이 일반 Python 함수라면:
def get_items():
    return {"items": []}
# → 이건 그냥 함수일 뿐, 웹 요청과 연결되지 않음

# 데코레이터를 붙이면:
@router.get("/items")
def get_items():
    return {"items": []}
# → 웹 브라우저에서 /items로 접근하면 이 함수가 실행됨!
```

### 2.2 HTTP 메서드 이해하기

웹에서 요청을 보낼 때는 "어떤 의도인지"를 나타내는 방식이 있습니다:

```python
from fastapi import APIRouter

router = APIRouter()

# ============================================================
# GET - 데이터 조회 (읽기만 함, 서버 데이터 변경 없음)
# ============================================================
@router.get("/items")  # 아이템 목록 가져오기
async def get_items():
    # 예: 데이터베이스에서 아이템들을 읽어옴
    return {"items": ["사과", "바나나", "체리"]}

# ============================================================
# POST - 새 데이터 생성
# ============================================================
@router.post("/items")  # 새 아이템 만들기
async def create_item():
    # 예: 새 아이템을 데이터베이스에 저장
    return {"message": "아이템이 생성되었습니다"}

# ============================================================
# PUT - 데이터 전체 수정
# ============================================================
@router.put("/items/1")  # 1번 아이템 전체 수정
async def update_item():
    # 예: 1번 아이템의 모든 정보를 새 정보로 교체
    return {"message": "아이템이 수정되었습니다"}

# ============================================================
# PATCH - 데이터 일부 수정
# ============================================================
@router.patch("/items/1")  # 1번 아이템 일부만 수정
async def partial_update_item():
    # 예: 1번 아이템의 이름만 변경
    return {"message": "아이템이 부분 수정되었습니다"}

# ============================================================
# DELETE - 데이터 삭제
# ============================================================
@router.delete("/items/1")  # 1번 아이템 삭제
async def delete_item():
    # 예: 1번 아이템을 데이터베이스에서 삭제
    return {"message": "아이템이 삭제되었습니다"}
```

**비유로 이해하기:**
- GET: 도서관에서 책 찾아보기 (책은 그대로)
- POST: 도서관에 새 책 기증하기 (책 추가됨)
- PUT: 책 전체를 새 책으로 교체하기
- PATCH: 책의 표지만 바꾸기
- DELETE: 도서관에서 책 폐기하기

### 2.3 async/await란?

Python만 사용하셨다면 `async`와 `await`가 낯설 수 있습니다.

```python
# ============================================================
# 일반 함수 (동기 방식)
# ============================================================
def normal_function():
    # 이 함수가 끝날 때까지 다른 일을 못 함
    result = do_something()  # 이게 끝나야
    return result            # 다음 줄 실행

# ============================================================
# 비동기 함수 (async 방식)
# ============================================================
async def async_function():
    # 기다리는 동안 다른 일을 할 수 있음
    result = await do_something()  # 기다리는 동안 다른 요청 처리 가능
    return result

# ============================================================
# 실제 예시로 이해하기
# ============================================================

# 상황: 커피숍에서 커피 주문

# 동기 방식 (일반 함수)
def order_coffee_sync():
    make_coffee()  # 커피 만들기 (3분)
    # → 3분 동안 아무것도 못 함, 다음 손님 대기
    return "커피 완성"

# 비동기 방식 (async 함수)
async def order_coffee_async():
    await make_coffee()  # 커피 만들기 (3분)
    # → 3분 동안 다른 손님 주문 받을 수 있음!
    return "커피 완성"
```

**FastAPI에서 async를 쓰는 이유:**
```python
# 100명이 동시에 접속하면?

# 동기 방식: 1명씩 처리 → 오래 걸림
@router.get("/data")
def get_data():  # async 없음
    data = fetch_from_database()  # 1초 걸림
    return data
# → 100명 처리하려면 100초 걸림

# 비동기 방식: 동시에 처리 → 빠름
@router.get("/data")
async def get_data():  # async 있음
    data = await fetch_from_database()  # 기다리는 동안 다른 요청 처리
    return data
# → 100명을 거의 동시에 처리 가능!
```

---

## 3. 경로 매개변수와 쿼리 매개변수

### 3.1 경로 매개변수 (Path Parameters)

URL 주소 안에 변수를 넣는 방법입니다.

```python
from fastapi import APIRouter

router = APIRouter()

# ============================================================
# 경로 매개변수 기본 사용법
# ============================================================
@router.get("/items/{item_id}")  # {item_id}가 경로 매개변수
async def get_item(item_id: int):  # 함수 인자로 받음
    # URL이 /items/5 이면 → item_id = 5
    # URL이 /items/100 이면 → item_id = 100
    return {"item_id": item_id}

# ↑ 코드 분석:
# @router.get("/items/{item_id}")
#   └── "/items/" 뒤에 오는 값을 item_id라는 이름으로 받겠다
#
# async def get_item(item_id: int):
#   └── item_id: int → 정수(int) 타입이어야 함
#                       "abc" 같은 문자가 오면 자동으로 에러!

# ============================================================
# 여러 경로 매개변수
# ============================================================
@router.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: int):
    # URL: /users/1/items/5
    # → user_id = 1, item_id = 5
    return {
        "user_id": user_id,
        "item_id": item_id
    }

# ============================================================
# 문자열 경로 매개변수
# ============================================================
@router.get("/users/{username}")
async def get_user_by_name(username: str):  # str 타입
    # URL: /users/john → username = "john"
    # URL: /users/홍길동 → username = "홍길동"
    return {"username": username}
```

### 3.2 쿼리 매개변수 (Query Parameters)

URL 뒤에 `?key=value` 형태로 붙는 매개변수입니다.

```python
from fastapi import APIRouter
from typing import Optional  # 선택적 매개변수를 위해 필요

router = APIRouter()

# ============================================================
# 쿼리 매개변수 기본 사용법
# ============================================================
@router.get("/search")
async def search(q: str):  # 필수 쿼리 매개변수
    # URL: /search?q=파이썬
    # → q = "파이썬"

    # URL: /search (q 없이)
    # → 에러 발생! (필수이므로)

    return {"검색어": q}

# ============================================================
# 선택적 쿼리 매개변수 (기본값 있음)
# ============================================================
@router.get("/items")
async def get_items(
    skip: int = 0,      # 기본값 0
    limit: int = 10     # 기본값 10
):
    # URL: /items
    # → skip = 0, limit = 10 (기본값 사용)

    # URL: /items?skip=5
    # → skip = 5, limit = 10

    # URL: /items?skip=5&limit=20
    # → skip = 5, limit = 20

    return {"skip": skip, "limit": limit}

# ============================================================
# Optional 사용 (None 허용)
# ============================================================
@router.get("/products")
async def get_products(
    category: Optional[str] = None,  # 없으면 None
    min_price: Optional[int] = None
):
    # URL: /products
    # → category = None, min_price = None

    # URL: /products?category=전자제품
    # → category = "전자제품", min_price = None

    result = {"category": category, "min_price": min_price}
    return result

# ============================================================
# 경로 + 쿼리 매개변수 함께 사용
# ============================================================
@router.get("/users/{user_id}/items")
async def get_user_items(
    user_id: int,           # 경로 매개변수 (필수)
    skip: int = 0,          # 쿼리 매개변수 (선택)
    limit: int = 10         # 쿼리 매개변수 (선택)
):
    # URL: /users/1/items?skip=0&limit=5
    # → user_id = 1, skip = 0, limit = 5

    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }
```

---

## 4. 요청 바디 (Request Body)

POST, PUT 등으로 데이터를 보낼 때 사용합니다.

### 4.1 Pydantic 모델이란?

데이터의 형태(스키마)를 정의하는 방법입니다.

```python
# ============================================================
# Pydantic 모델 기본
# ============================================================
from pydantic import BaseModel  # Pydantic에서 BaseModel 가져오기
from typing import Optional

# 데이터 형태 정의
class ItemCreate(BaseModel):  # BaseModel을 상속
    """아이템 생성 시 필요한 데이터 형태"""

    title: str                        # 필수: 문자열
    description: Optional[str] = None  # 선택: 문자열 또는 None
    price: float                       # 필수: 실수
    quantity: int = 1                  # 선택: 정수, 기본값 1

# ↑ 이 클래스가 하는 일:
# 1. 들어온 데이터가 정의한 형태와 맞는지 자동 검사
# 2. 타입이 다르면 자동 변환 시도 (예: "100" → 100)
# 3. 변환 불가능하면 에러 발생
```

### 4.2 요청 바디 사용하기

```python
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

# ============================================================
# 데이터 모델 정의
# ============================================================
class ItemCreate(BaseModel):
    title: str = Field(
        ...,                    # ... 은 "필수"라는 의미
        min_length=1,           # 최소 1글자
        max_length=200,         # 최대 200글자
        description="아이템 제목"  # API 문서에 표시될 설명
    )

    description: Optional[str] = Field(
        default=None,           # 기본값 None
        max_length=1000,
        description="아이템 설명"
    )

    price: float = Field(
        ...,                    # 필수
        gt=0,                   # greater than 0 (0보다 커야 함)
        description="가격"
    )

    quantity: int = Field(
        default=1,              # 기본값 1
        ge=0,                   # greater or equal (0 이상)
        le=1000,                # less or equal (1000 이하)
        description="수량"
    )

# Field 옵션 설명:
# - ... : 필수 필드
# - default=값 : 기본값 설정
# - min_length, max_length : 문자열 길이 제한
# - gt, ge, lt, le : 숫자 범위 제한
#   - gt: greater than (초과)
#   - ge: greater or equal (이상)
#   - lt: less than (미만)
#   - le: less or equal (이하)

# ============================================================
# 요청 바디를 받는 라우터
# ============================================================
@router.post("/items")
async def create_item(item: ItemCreate):  # item 매개변수에 ItemCreate 타입
    # 클라이언트가 보낸 JSON:
    # {
    #     "title": "노트북",
    #     "description": "맥북 프로",
    #     "price": 2500000,
    #     "quantity": 5
    # }

    # → item.title = "노트북"
    # → item.description = "맥북 프로"
    # → item.price = 2500000
    # → item.quantity = 5

    # 잘못된 데이터가 오면?
    # {"title": "", "price": -100}
    # → 자동으로 에러 응답!
    # → "title은 1글자 이상이어야 합니다"
    # → "price는 0보다 커야 합니다"

    return {
        "message": "아이템 생성됨",
        "item": item  # Pydantic 모델을 그대로 반환 가능
    }

# ============================================================
# 모델 데이터를 딕셔너리로 변환
# ============================================================
@router.post("/items/dict")
async def create_item_dict(item: ItemCreate):
    # model_dump(): 모델을 딕셔너리로 변환
    item_dict = item.model_dump()
    # {"title": "노트북", "description": "맥북 프로", ...}

    # 특정 필드만 가져오기
    item_partial = item.model_dump(include={"title", "price"})
    # {"title": "노트북", "price": 2500000}

    # 특정 필드 제외하기
    item_without_desc = item.model_dump(exclude={"description"})
    # {"title": "노트북", "price": 2500000, "quantity": 5}

    return item_dict
```

### 4.3 Form 데이터 받기

HTML 폼에서 데이터를 받을 때 사용합니다.

```python
from fastapi import APIRouter, Form

router = APIRouter()

# ============================================================
# Form 데이터 받기
# ============================================================
@router.post("/login")
async def login(
    # Form(...) : 필수 폼 필드
    username: str = Form(...),
    password: str = Form(...)
):
    # HTML 폼:
    # <form method="post" action="/login">
    #     <input name="username" type="text">
    #     <input name="password" type="password">
    #     <button type="submit">로그인</button>
    # </form>

    # 폼 제출 시:
    # username = "john"
    # password = "1234"

    # 주의: Form()을 사용하려면 python-multipart 설치 필요
    # pip install python-multipart

    return {"username": username}

# ============================================================
# Form vs JSON 차이
# ============================================================

# Form 데이터: HTML <form> 태그에서 전송
# Content-Type: application/x-www-form-urlencoded
# 형태: username=john&password=1234

# JSON 데이터: JavaScript에서 fetch/axios로 전송
# Content-Type: application/json
# 형태: {"username": "john", "password": "1234"}
```

---

## 5. 응답 (Response)

### 5.1 응답 타입 지정

```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

router = APIRouter()

# ============================================================
# 응답 모델 정의
# ============================================================
class ItemResponse(BaseModel):
    id: int
    title: str
    price: float

# ============================================================
# response_model: 응답 형태 지정 및 검증
# ============================================================
@router.get("/items/{id}", response_model=ItemResponse)
async def get_item(id: int):
    # response_model을 지정하면:
    # 1. 반환 데이터가 ItemResponse 형태인지 검증
    # 2. API 문서에 응답 형태가 표시됨
    # 3. 지정하지 않은 필드는 자동으로 제외됨

    return {
        "id": id,
        "title": "노트북",
        "price": 2500000,
        "secret_field": "이건 응답에 포함 안됨"  # ItemResponse에 없으므로 제외
    }

# ============================================================
# HTML 응답 반환
# ============================================================
@router.get("/page", response_class=HTMLResponse)
async def get_page():
    # response_class=HTMLResponse로 지정하면
    # 브라우저가 HTML로 인식하고 화면에 렌더링함

    html_content = """
    <html>
        <head><title>안녕하세요</title></head>
        <body>
            <h1>환영합니다!</h1>
            <p>이것은 HTML 페이지입니다.</p>
        </body>
    </html>
    """
    return html_content

# ============================================================
# 상태 코드 지정
# ============================================================
@router.post("/items", status_code=201)  # 201 Created
async def create_item():
    # status_code=201: 새 리소스 생성됨을 나타냄

    # 자주 사용하는 상태 코드:
    # 200: OK (기본값)
    # 201: Created (생성됨)
    # 204: No Content (내용 없음)
    # 400: Bad Request (잘못된 요청)
    # 401: Unauthorized (인증 필요)
    # 403: Forbidden (권한 없음)
    # 404: Not Found (찾을 수 없음)
    # 500: Internal Server Error (서버 에러)

    return {"message": "아이템 생성됨"}

# ============================================================
# 커스텀 헤더 추가
# ============================================================
@router.get("/custom-header")
async def custom_header():
    # JSONResponse 객체를 직접 만들어서 헤더 추가
    response = JSONResponse(
        content={"message": "헤더가 포함된 응답"}
    )

    # 커스텀 헤더 추가
    response.headers["X-Custom-Header"] = "커스텀 값"
    response.headers["X-Process-Time"] = "0.5초"

    return response
```

---

## 6. 의존성 주입 (Dependency Injection)

의존성 주입은 FastAPI의 핵심 기능 중 하나입니다.

### 6.1 의존성이란?

```python
# ============================================================
# 의존성 주입이 없을 때의 문제
# ============================================================

# 나쁜 예: 매번 데이터베이스 연결을 직접 생성
@router.get("/items")
async def get_items():
    db = create_database_connection()  # 매번 연결 생성
    items = db.query("SELECT * FROM items")
    db.close()  # 연결 닫기
    return items

@router.get("/users")
async def get_users():
    db = create_database_connection()  # 또 생성
    users = db.query("SELECT * FROM users")
    db.close()  # 또 닫기
    return users

# 문제점:
# 1. 코드 중복
# 2. 연결 닫는 것을 잊어버릴 수 있음
# 3. 테스트하기 어려움
```

### 6.2 의존성 함수 만들기

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# ============================================================
# 의존성 함수 정의
# ============================================================
async def get_db():
    """데이터베이스 세션을 생성하고 반환하는 의존성 함수"""

    # 1. 세션 생성
    session = AsyncSession()  # 데이터베이스 세션 생성

    try:
        # 2. 세션을 "yield"로 반환
        yield session
        # ↑ yield: 세션을 반환하고, 요청 처리가 끝날 때까지 대기

        # 3. 요청 처리가 끝나면 아래 코드 실행
        await session.commit()  # 변경사항 저장

    except Exception:
        # 4. 에러 발생 시 롤백
        await session.rollback()
        raise

    finally:
        # 5. 항상 세션 닫기
        await session.close()

# ============================================================
# 의존성 사용하기
# ============================================================
@router.get("/items")
async def get_items(
    db: AsyncSession = Depends(get_db)  # 의존성 주입!
    #  ↑                  ↑
    #  db 변수에      get_db 함수의 결과가 들어옴
):
    # db를 사용하여 데이터 조회
    items = await db.execute("SELECT * FROM items")
    return items

# 동작 순서:
# 1. /items 요청 들어옴
# 2. Depends(get_db)가 get_db() 함수 호출
# 3. get_db()가 session을 yield
# 4. session이 db 변수에 할당됨
# 5. get_items() 함수 본문 실행
# 6. get_items() 완료 후 get_db()의 finally 블록 실행
```

### 6.3 Annotated를 사용한 의존성

Python 3.9+에서 더 깔끔하게 의존성을 정의할 수 있습니다.

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# 타입 별칭으로 의존성 정의
# ============================================================

# Annotated: 타입에 추가 정보를 붙이는 Python 기능
# Annotated[타입, 추가정보]
DbSession = Annotated[AsyncSession, Depends(get_db)]
#           ↑           ↑              ↑
#         기본 타입   추가 정보    Depends(get_db)를 붙임

# ============================================================
# 사용하기
# ============================================================

# 기존 방식
@router.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    pass

# Annotated 방식 (더 깔끔!)
@router.get("/items")
async def get_items(db: DbSession):  # 훨씬 간단!
    pass

# ============================================================
# 여러 의존성 조합
# ============================================================
# 현재 로그인한 사용자를 가져오는 의존성
async def get_current_user(db: DbSession):
    # 토큰에서 사용자 정보 추출
    user = await get_user_from_token(db)
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/my-items")
async def get_my_items(
    db: DbSession,            # 데이터베이스 세션
    user: CurrentUser         # 현재 로그인한 사용자
):
    # user.id로 내 아이템만 조회
    items = await db.query(Item).filter(Item.owner_id == user.id).all()
    return items
```

---

## 7. 에러 처리

### 7.1 HTTPException

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

# ============================================================
# 기본 HTTPException 사용
# ============================================================
@router.get("/items/{item_id}")
async def get_item(item_id: int):
    # 아이템 조회
    item = await find_item(item_id)

    # 아이템이 없으면 404 에러 발생
    if item is None:
        raise HTTPException(
            status_code=404,  # HTTP 상태 코드
            detail="아이템을 찾을 수 없습니다"  # 에러 메시지
        )
        # ↑ raise: 예외를 발생시키고 함수 실행 중단

        # 클라이언트가 받는 응답:
        # HTTP 404 Not Found
        # {"detail": "아이템을 찾을 수 없습니다"}

    return item

# ============================================================
# 다양한 에러 상황
# ============================================================
@router.post("/items")
async def create_item(item: ItemCreate, user: CurrentUser):

    # 권한 체크
    if not user.can_create_item:
        raise HTTPException(
            status_code=403,  # Forbidden
            detail="아이템을 생성할 권한이 없습니다"
        )

    # 중복 체크
    existing = await find_item_by_title(item.title)
    if existing:
        raise HTTPException(
            status_code=400,  # Bad Request
            detail=f"'{item.title}' 제목의 아이템이 이미 존재합니다"
        )

    # 정상 처리
    new_item = await save_item(item)
    return new_item

# ============================================================
# 헤더 포함 에러
# ============================================================
@router.get("/protected")
async def protected_route():
    raise HTTPException(
        status_code=401,
        detail="인증이 필요합니다",
        headers={"WWW-Authenticate": "Bearer"}  # 추가 헤더
    )
```

### 7.2 커스텀 예외

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# ============================================================
# 커스텀 예외 클래스 정의
# ============================================================
class ItemNotFoundError(Exception):
    """아이템을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.message = f"아이템 {item_id}를 찾을 수 없습니다"

class NotEnoughPermissionError(Exception):
    """권한이 부족할 때 발생하는 예외"""
    def __init__(self, action: str):
        self.action = action
        self.message = f"'{action}' 작업을 수행할 권한이 없습니다"

# ============================================================
# 예외 핸들러 등록
# ============================================================
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    """ItemNotFoundError가 발생하면 이 함수가 처리"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "item_not_found",
            "message": exc.message,
            "item_id": exc.item_id
        }
    )

@app.exception_handler(NotEnoughPermissionError)
async def permission_error_handler(request: Request, exc: NotEnoughPermissionError):
    return JSONResponse(
        status_code=403,
        content={
            "error": "permission_denied",
            "message": exc.message,
            "action": exc.action
        }
    )

# ============================================================
# 커스텀 예외 사용
# ============================================================
@router.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await find_item(item_id)

    if item is None:
        raise ItemNotFoundError(item_id)
        # → item_not_found_handler가 처리
        # → 404 응답 + 상세 에러 정보

    return item
```

---

## 8. 이 프로젝트의 FastAPI 패턴

### 8.1 라우터 구조

이 프로젝트는 3가지 유형의 라우터를 사용합니다.

```
app/
├── api/              # REST API (JSON 응답)
│   └── v1/
│       ├── router.py    # 모든 API 라우터 통합
│       ├── auth.py      # 로그인, 회원가입 API
│       ├── items.py     # 아이템 CRUD API
│       └── users.py     # 사용자 관련 API
│
├── pages/            # 페이지 라우터 (HTML 응답)
│   ├── router.py        # 페이지 라우터 통합
│   ├── home.py          # 홈페이지
│   ├── auth.py          # 로그인/회원가입 페이지
│   └── dashboard.py     # 대시보드 페이지
│
└── partials/         # HTMX 파셜 라우터 (HTML 조각 응답)
    ├── router.py        # 파셜 라우터 통합
    ├── items.py         # 아이템 목록/수정 등 HTML 조각
    ├── modals.py        # 모달 내용
    └── toasts.py        # 토스트 알림
```

### 8.2 페이지 라우터 예제

```python
# app/pages/home.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates  # Jinja2 템플릿 엔진

router = APIRouter()

# ============================================================
# 홈페이지 라우터
# ============================================================
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    메인 홈페이지를 렌더링합니다.

    - response_class=HTMLResponse: HTML을 반환한다고 선언
    - request: Request: FastAPI가 자동으로 현재 요청 정보를 넣어줌
    """

    # templates.TemplateResponse: Jinja2 템플릿 렌더링
    return templates.TemplateResponse(
        request=request,          # 요청 객체 (템플릿에서 사용 가능)
        name="pages/home.html",   # 렌더링할 템플릿 파일 경로
        context={                 # 템플릿에 전달할 데이터
            "title": "홈",
            "description": "FastAPI + Jinja2 + HTMX 보일러플레이트"
        }
    )

    # → templates/pages/home.html 파일이 렌더링됨
    # → 템플릿 내에서 {{ title }}, {{ description }} 사용 가능
```

### 8.3 파셜 라우터 예제

```python
# app/partials/items.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from app.services.item import ItemService
from app.api.deps import DbSession, CurrentUser

router = APIRouter(prefix="/partials/items")
# prefix: 이 라우터의 모든 경로 앞에 "/partials/items"가 붙음

# ============================================================
# 아이템 목록 파셜
# ============================================================
@router.get("", response_class=HTMLResponse)
async def get_items_partial(
    request: Request,
    db: DbSession,
    user: CurrentUser
):
    """
    아이템 목록을 HTML 조각으로 반환합니다.
    HTMX가 이 응답을 받아서 페이지의 일부분만 교체합니다.

    경로: GET /partials/items
    """

    # 서비스를 통해 아이템 목록 조회
    service = ItemService(db)
    items = await service.get_all(owner_id=user.id)

    # HTML 조각 반환 (전체 페이지가 아닌 부분만)
    return templates.TemplateResponse(
        request=request,
        name="partials/items/list.html",  # 부분 템플릿
        context={"items": items}
    )

# ============================================================
# 아이템 삭제 파셜
# ============================================================
@router.delete("/{item_id}", response_class=HTMLResponse)
async def delete_item(
    item_id: int,
    db: DbSession,
    user: CurrentUser
):
    """
    아이템을 삭제하고 빈 응답을 반환합니다.
    HTMX가 hx-swap="outerHTML"로 해당 요소를 빈 내용으로 교체합니다.

    경로: DELETE /partials/items/{item_id}
    """

    service = ItemService(db)
    await service.delete(item_id, owner_id=user.id)

    # 빈 응답 + 토스트 알림 트리거
    response = HTMLResponse(content="")  # 빈 HTML

    # HX-Trigger 헤더: 클라이언트에서 이벤트 발생시킴
    response.headers["HX-Trigger"] = json.dumps({
        "showToast": {
            "type": "success",
            "message": "아이템이 삭제되었습니다"
        }
    })

    return response
```

### 8.4 서비스 레이어

```python
# app/services/item.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate

class ItemService:
    """
    아이템 관련 비즈니스 로직을 담당하는 서비스 클래스

    서비스 레이어를 사용하는 이유:
    1. 비즈니스 로직과 라우터 분리
    2. 코드 재사용성 향상
    3. 테스트 용이성
    """

    def __init__(self, db: AsyncSession):
        """
        생성자: 데이터베이스 세션을 받아서 저장

        db: AsyncSession - 데이터베이스와 통신하는 세션
        """
        self.db = db  # 인스턴스 변수로 저장

    async def get_all(self, owner_id: int) -> list[Item]:
        """
        특정 사용자의 모든 아이템을 조회합니다.

        owner_id: 아이템 소유자의 ID
        반환: 아이템 목록
        """
        # select(Item): "SELECT * FROM items" 와 비슷
        # .where(): "WHERE owner_id = ?" 조건 추가
        query = select(Item).where(Item.owner_id == owner_id)

        # execute(): 쿼리 실행
        result = await self.db.execute(query)

        # scalars().all(): 결과를 Item 객체 리스트로 변환
        return list(result.scalars().all())

    async def create(self, item_in: ItemCreate, owner_id: int) -> Item:
        """
        새 아이템을 생성합니다.

        item_in: 생성할 아이템 정보 (Pydantic 모델)
        owner_id: 아이템 소유자 ID
        반환: 생성된 아이템
        """
        # Item 모델 인스턴스 생성
        item = Item(
            **item_in.model_dump(),  # Pydantic 모델을 딕셔너리로 변환
            owner_id=owner_id        # 소유자 ID 추가
        )

        # **item_in.model_dump() 설명:
        # item_in = ItemCreate(title="노트북", description="맥북")
        # item_in.model_dump() → {"title": "노트북", "description": "맥북"}
        # **딕셔너리 → title="노트북", description="맥북" (풀어서 전달)

        # 세션에 추가
        self.db.add(item)

        # flush: 데이터베이스에 쿼리 전송 (아직 commit은 아님)
        # → item.id가 생성됨
        await self.db.flush()

        return item
```

---

## 9. 비동기 프로그래밍 심화

### 9.1 여러 작업 동시 실행

```python
import asyncio

# ============================================================
# asyncio.gather: 여러 비동기 작업을 동시에 실행
# ============================================================
async def fetch_all_data():
    # 순차 실행 (느림)
    # users = await get_users()     # 1초 대기
    # items = await get_items()     # 1초 대기
    # orders = await get_orders()   # 1초 대기
    # → 총 3초 걸림

    # 동시 실행 (빠름)
    users, items, orders = await asyncio.gather(
        get_users(),    # 1초
        get_items(),    # 1초  → 동시에 실행
        get_orders()    # 1초
    )
    # → 총 1초 걸림 (가장 오래 걸리는 작업 시간)

    return {"users": users, "items": items, "orders": orders}

# ============================================================
# 실제 라우터에서 사용
# ============================================================
@router.get("/dashboard")
async def dashboard(db: DbSession, user: CurrentUser):
    # 대시보드에 필요한 여러 데이터를 동시에 조회
    user_stats, recent_items, notifications = await asyncio.gather(
        get_user_stats(db, user.id),
        get_recent_items(db, user.id),
        get_notifications(db, user.id)
    )

    return templates.TemplateResponse(
        request=request,
        name="pages/dashboard.html",
        context={
            "user_stats": user_stats,
            "recent_items": recent_items,
            "notifications": notifications
        }
    )
```

---

## 10. 테스트

### 10.1 기본 테스트 작성

```python
# tests/test_items.py

import pytest
from httpx import AsyncClient

# ============================================================
# pytest 마커: 비동기 테스트임을 표시
# ============================================================
@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    """
    아이템 목록 조회 API 테스트

    client: 테스트용 HTTP 클라이언트 (fixture로 주입)
    """

    # GET 요청 보내기
    response = await client.get("/api/v1/items")

    # 응답 상태 코드 확인
    assert response.status_code == 200
    # assert: 조건이 True가 아니면 테스트 실패

    # 응답 데이터 확인
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, auth_headers: dict):
    """
    아이템 생성 API 테스트

    auth_headers: 인증 헤더 (로그인된 상태를 시뮬레이션)
    """

    # 생성할 아이템 데이터
    new_item = {
        "title": "테스트 아이템",
        "description": "테스트 설명",
        "price": 10000
    }

    # POST 요청 보내기
    response = await client.post(
        "/api/v1/items",
        json=new_item,        # JSON 바디
        headers=auth_headers  # 인증 헤더
    )

    # 생성 성공 확인
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "테스트 아이템"
    assert "id" in data  # ID가 생성되었는지 확인
```

---

## 11. 유용한 팁

### 11.1 백그라운드 작업

```python
from fastapi import BackgroundTasks

# ============================================================
# 이메일 발송 같은 시간이 걸리는 작업을 백그라운드로 처리
# ============================================================
async def send_email_task(email: str, subject: str, body: str):
    """실제 이메일 발송 작업"""
    # 이 작업은 시간이 걸릴 수 있음
    await email_service.send(email, subject, body)

@router.post("/register")
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks  # FastAPI가 자동으로 주입
):
    # 1. 사용자 생성
    user = await create_user(user_data)

    # 2. 환영 이메일 발송을 백그라운드로 등록
    background_tasks.add_task(
        send_email_task,          # 실행할 함수
        user.email,               # 함수 인자들
        "가입을 환영합니다!",
        "우리 서비스에 가입해주셔서 감사합니다."
    )

    # 3. 즉시 응답 (이메일은 나중에 발송됨)
    return {"message": "회원가입이 완료되었습니다"}

    # → 사용자는 이메일 발송을 기다리지 않고 바로 응답을 받음
    # → 이메일은 백그라운드에서 발송됨
```

### 11.2 라이프사이클 이벤트

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# ============================================================
# 앱 시작/종료 시 실행할 코드
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ========== 앱 시작 시 ==========
    print("앱이 시작됩니다!")

    # 데이터베이스 초기화
    await init_database()

    # 캐시 연결
    await connect_redis()

    yield  # 앱이 실행되는 동안 여기서 대기

    # ========== 앱 종료 시 ==========
    print("앱이 종료됩니다!")

    # 연결 정리
    await close_redis()
    await close_database()

# FastAPI 앱에 lifespan 등록
app = FastAPI(lifespan=lifespan)
```

---

## 12. 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com) - 가장 중요한 자료
- [FastAPI 튜토리얼 (한국어)](https://fastapi.tiangolo.com/ko/tutorial/)
- [Starlette 문서](https://www.starlette.io) - FastAPI의 기반 프레임워크
- [Pydantic 문서](https://docs.pydantic.dev) - 데이터 검증 라이브러리

### 12.1 공부 순서 추천

1. 먼저 기본 라우터 만들어보기 (`@router.get`, `@router.post`)
2. 경로/쿼리 매개변수 이해하기
3. Pydantic 모델로 요청 바디 받기
4. 의존성 주입 이해하기
5. 비동기 프로그래밍 심화
6. 테스트 작성하기
