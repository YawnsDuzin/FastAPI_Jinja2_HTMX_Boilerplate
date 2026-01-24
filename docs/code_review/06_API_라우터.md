# 06. API 라우터

## 6.1 개요

API 라우터는 **REST API 엔드포인트**를 정의합니다. JSON 형식의 요청을 받아 JSON 형식으로 응답하며, 외부 클라이언트(모바일 앱, 다른 서비스 등)에서도 사용할 수 있습니다.

### 관련 파일

- `app/api/deps.py` - 의존성 주입
- `app/api/v1/router.py` - 라우터 통합
- `app/api/v1/auth.py` - 인증 API
- `app/api/v1/items.py` - 아이템 API
- `app/api/v1/users.py` - 사용자 API

### URL 구조

```
/api/v1/
├── auth/
│   ├── POST /register      # 회원가입
│   ├── POST /login         # 로그인
│   ├── POST /logout        # 로그아웃
│   ├── POST /refresh       # 토큰 갱신
│   └── GET  /me            # 현재 사용자 정보
│
├── users/
│   ├── GET  /              # 사용자 목록 (관리자)
│   ├── GET  /{id}          # 사용자 상세
│   ├── PATCH /me           # 내 정보 수정
│   ├── POST /me/change-password  # 비밀번호 변경
│   └── DELETE /{id}        # 사용자 삭제 (관리자)
│
└── items/
    ├── GET  /              # 아이템 목록
    ├── GET  /paginated     # 아이템 목록 (페이지네이션)
    ├── GET  /{id}          # 아이템 상세
    ├── POST /              # 아이템 생성
    ├── PATCH /{id}         # 아이템 수정
    ├── DELETE /{id}        # 아이템 삭제
    └── POST /{id}/toggle   # 활성/비활성 토글
```

---

## 6.2 의존성 주입 (app/api/deps.py)

### 6.2.1 의존성 주입이란?

의존성 주입(Dependency Injection)은 함수가 필요로 하는 객체를 외부에서 제공받는 패턴입니다.

```python
# Without DI (직접 생성)
@app.get("/users")
async def get_users():
    db = create_session()  # 직접 생성 - 테스트 어려움
    users = await db.query(User).all()
    return users

# With DI (주입받음)
@app.get("/users")
async def get_users(db: DbSession):  # 자동 주입 - 테스트 용이
    users = await db.query(User).all()
    return users
```

### 6.2.2 타입 별칭 정의

```python
from typing import Annotated, Optional
from fastapi import Cookie, Depends

# 데이터베이스 세션 의존성
DbSession = Annotated[AsyncSession, Depends(get_db)]

# 인증 필수 (로그인 안하면 401)
CurrentUser = Annotated[User, Depends(get_current_user)]

# 인증 선택 (로그인 안해도 OK, None 반환)
CurrentUserOptional = Annotated[Optional[User], Depends(get_current_user_optional)]

# 관리자 필수 (관리자 아니면 403)
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]
```

### 6.2.3 토큰 추출 함수

```python
async def get_token_from_cookie(
    access_token: Annotated[Optional[str], Cookie()] = None,
) -> Optional[str]:
    """
    httpOnly 쿠키에서 JWT 토큰 추출

    Cookie() 파라미터:
    - 함수 파라미터 이름(access_token)과 쿠키 이름이 동일해야 함
    - Optional[str]로 선언하여 쿠키 없어도 에러 발생 X
    """
    return access_token
```

### 6.2.4 현재 사용자 조회

```python
async def get_current_user(
    db: DbSession,
    token: Annotated[Optional[str], Depends(get_token_from_cookie)],
) -> User:
    """
    현재 인증된 사용자 조회

    흐름:
    1. 쿠키에서 토큰 추출
    2. JWT 토큰 검증
    3. 페이로드에서 사용자 ID 추출
    4. DB에서 사용자 조회
    5. 활성 상태 확인
    """
    # 토큰 없음 → 401
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 토큰 검증
    payload = verify_token(token, token_type="access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
        )

    # 사용자 조회
    user_id = int(payload["sub"])
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비활성화된 계정입니다.",
        )

    return user
```

### 6.2.5 의존성 체이닝

```
get_current_superuser
        │
        │ Depends
        ▼
get_current_user
        │
        │ Depends
        ▼
get_token_from_cookie
        │
        │ Cookie()
        ▼
    HTTP 요청 쿠키
```

---

## 6.3 인증 API (app/api/v1/auth.py)

### 6.3.1 라우터 생성

```python
from fastapi import APIRouter, Response, Depends
from typing import Annotated

router = APIRouter()
```

### 6.3.2 회원가입 엔드포인트

```python
@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    회원가입

    - **email**: 이메일 (유일해야 함)
    - **username**: 사용자명 (유일해야 함)
    - **password**: 비밀번호 (8자 이상)
    - **full_name**: 이름 (선택)
    """
    user = await auth_service.register(user_in)
    return user
```

### 6.3.3 로그인 엔드포인트

```python
@router.post("/login", response_model=Token)
async def login(
    response: Response,
    user_in: UserLogin,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    로그인

    인증 성공 시 JWT 토큰을 httpOnly 쿠키에 설정합니다.
    """
    tokens = await auth_service.login(user_in.email, user_in.password)

    # 쿠키 설정 (httpOnly, secure)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,      # JavaScript에서 접근 불가 (XSS 방지)
        secure=False,       # Production에서는 True (HTTPS만 허용)
        samesite="lax",     # CSRF 방어
        max_age=3600,       # 1시간
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800,     # 7일
    )

    return tokens
```

### 6.3.4 로그아웃 엔드포인트

```python
@router.post("/logout")
async def logout(response: Response):
    """
    로그아웃

    쿠키에서 토큰을 제거합니다.
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "로그아웃되었습니다."}
```

### 6.3.5 현재 사용자 정보

```python
@router.get("/me", response_model=User)
async def get_current_user_info(current_user: CurrentUser):
    """
    현재 사용자 정보

    인증된 사용자의 프로필 정보를 반환합니다.
    """
    return current_user
```

---

## 6.4 아이템 API (app/api/v1/items.py)

### 6.4.1 목록 조회

```python
@router.get("", response_model=List[Item])
async def get_items(
    current_user: CurrentUser,  # 인증 필수
    item_service: Annotated[ItemService, Depends(get_item_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    """
    아이템 목록 조회

    현재 사용자의 아이템만 조회됩니다.
    """
    items = await item_service.get_all(
        owner_id=current_user.id,  # 본인 아이템만
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
    )
    return items
```

### 6.4.2 페이지네이션 조회

```python
@router.get("/paginated", response_model=PaginatedResponse[Item])
async def get_items_paginated(
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    """아이템 목록 조회 (페이지네이션)"""
    skip = (page - 1) * size

    items = await item_service.get_all(
        owner_id=current_user.id,
        skip=skip,
        limit=size,
        search=search,
        is_active=is_active,
    )
    total = await item_service.count(
        owner_id=current_user.id,
        search=search,
        is_active=is_active,
    )

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=page,
        size=size,
    )
```

### 6.4.3 상세 조회

```python
@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 상세 조회"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    return item
```

### 6.4.4 생성

```python
@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 생성"""
    item = await item_service.create(item_in, current_user)
    return item
```

### 6.4.5 수정

```python
@router.patch("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 수정"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    updated_item = await item_service.update(item, item_in)
    return updated_item
```

### 6.4.6 삭제

```python
@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 삭제"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    await item_service.delete(item)
    return {"message": "아이템이 삭제되었습니다."}
```

---

## 6.5 사용자 API (app/api/v1/users.py)

### 6.5.1 권한 기반 접근 제어

```python
@router.get("", response_model=List[User])
async def get_users(
    current_user: CurrentSuperuser,  # 관리자만 접근 가능
    user_service: Annotated[UserService, Depends(get_user_service)],
    skip: int = 0,
    limit: int = 100,
):
    """사용자 목록 조회 (관리자 전용)"""
    users = await user_service.get_all(skip=skip, limit=limit)
    return users


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: CurrentSuperuser,  # 관리자만
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """사용자 삭제 (관리자 전용)"""
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 자기 자신 삭제 방지
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="자기 자신은 삭제할 수 없습니다.")

    await user_service.delete(user)
    return {"message": "사용자가 삭제되었습니다."}
```

---

## 6.6 라우터 통합 (app/api/v1/router.py)

```python
from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.items import router as items_router
from app.api.v1.users import router as users_router

api_router = APIRouter()

# 라우터 등록
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(items_router, prefix="/items", tags=["items"])
```

### 결과 URL 구조

```
/api/v1 (main.py에서 설정)
    │
    ├── /auth (router.py에서 설정)
    │   ├── /register
    │   └── /login
    │
    ├── /users
    │   └── /me
    │
    └── /items
        └── /{item_id}
```

---

## 6.7 API 응답 예시

### 회원가입 성공

```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "newuser",
    "password": "securepassword123",
    "full_name": "홍길동"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "email": "user@example.com",
    "username": "newuser",
    "full_name": "홍길동",
    "avatar_url": null,
    "is_active": true,
    "is_superuser": false,
    "is_verified": false,
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
}
```

### 로그인 성공

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: access_token=eyJ...; HttpOnly; Path=/; SameSite=Lax
Set-Cookie: refresh_token=eyJ...; HttpOnly; Path=/; SameSite=Lax

{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
}
```

### 인증 실패

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "detail": "이메일 또는 비밀번호가 올바르지 않습니다."
}
```
