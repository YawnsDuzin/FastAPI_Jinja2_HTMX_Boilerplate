# 아키텍처 설명

## 1. 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Browser)                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │  HTML   │  │  HTMX   │  │Alpine.js│  │  TailwindCSS    │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Middleware Layer                      ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  ││
│  │  │  CORS   │  │ Session │  │Exception│                  ││
│  │  └─────────┘  └─────────┘  └─────────┘                  ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │                     Router Layer                         ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  ││
│  │  │ API v1  │  │  Pages  │  │Partials │                  ││
│  │  │(JSON)   │  │ (HTML)  │  │ (HTML)  │                  ││
│  │  └─────────┘  └─────────┘  └─────────┘                  ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Service Layer                         ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  ││
│  │  │AuthServ │  │UserServ │  │ItemServ │                  ││
│  │  └─────────┘  └─────────┘  └─────────┘                  ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Repository Layer                       ││
│  │  ┌─────────────────┐  ┌─────────────────┐               ││
│  │  │  SQLAlchemy ORM │  │    Pydantic     │               ││
│  │  └─────────────────┘  └─────────────────┘               ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Database Layer                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │          SQLite / PostgreSQL / MySQL                     ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 2. 요청 흐름

### 2.1 페이지 요청 (전체 HTML)

```
Client → GET /dashboard
    → Pages Router (app/pages/dashboard.py)
        → 인증 확인 (Depends)
        → Service Layer (비즈니스 로직)
        → templates.TemplateResponse
            → Jinja2 렌더링
    ← 전체 HTML 페이지
```

### 2.2 HTMX 파셜 요청 (부분 HTML)

```
Client → GET /partials/items (HX-Request: true)
    → Partials Router (app/partials/items.py)
        → 인증 확인
        → Service Layer
        → templates.TemplateResponse
            → 파셜 템플릿 렌더링
    ← 부분 HTML
Client → DOM 업데이트 (hx-target, hx-swap)
```

### 2.3 API 요청 (JSON)

```
Client → POST /api/v1/items
    → API Router (app/api/v1/items.py)
        → 인증 확인
        → Pydantic 검증
        → Service Layer
        → 데이터베이스 작업
    ← JSON 응답
```

## 3. 계층별 책임

### 3.1 Router Layer

```
app/
├── api/v1/          # REST API (JSON 응답)
│   ├── auth.py      # 인증 API
│   ├── items.py     # 아이템 CRUD API
│   └── users.py     # 사용자 API
├── pages/           # HTML 페이지 (전체 페이지)
│   ├── home.py      # 홈페이지
│   ├── auth.py      # 로그인/회원가입
│   └── dashboard.py # 대시보드
└── partials/        # HTMX 파셜 (부분 HTML)
    ├── items.py     # 아이템 파셜
    ├── modals.py    # 모달 파셜
    └── toasts.py    # 토스트 파셜
```

**책임:**
- HTTP 요청 처리
- 입력 검증 (Pydantic)
- 응답 형식 결정 (JSON/HTML)
- 의존성 주입 받기

### 3.2 Service Layer

```
app/services/
├── auth.py    # 인증 로직 (로그인, 토큰 관리)
├── user.py    # 사용자 CRUD
└── item.py    # 아이템 CRUD
```

**책임:**
- 비즈니스 로직 구현
- 데이터베이스 작업 조합
- 트랜잭션 관리
- 예외 발생

### 3.3 Model Layer

```
app/models/
├── base.py    # 기본 모델 클래스
├── user.py    # 사용자 모델
└── item.py    # 아이템 모델
```

**책임:**
- 데이터베이스 스키마 정의
- 관계 정의
- 데이터 제약 조건

### 3.4 Schema Layer

```
app/schemas/
├── common.py  # 공통 스키마
├── user.py    # 사용자 스키마
└── item.py    # 아이템 스키마
```

**책임:**
- API 요청/응답 데이터 검증
- 직렬화/역직렬화
- 문서화

## 4. 의존성 흐름

```
Router
  ↓ Depends()
Service
  ↓ Constructor
Repository (SQLAlchemy Session)
  ↓
Database
```

### 4.1 의존성 주입 예시

```python
# app/api/deps.py
async def get_current_user(
    db: DbSession,
    token: str = Depends(get_token_from_cookie),
) -> User:
    # 토큰 검증 및 사용자 반환
    ...

CurrentUser = Annotated[User, Depends(get_current_user)]

# 라우터에서 사용
@router.get("/items")
async def get_items(
    current_user: CurrentUser,  # 자동 주입
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    return await item_service.get_all(owner_id=current_user.id)
```

## 5. 데이터 흐름

### 5.1 인증 흐름

```
1. 로그인 요청
   POST /api/v1/auth/login
   {email, password}

2. 인증 처리
   AuthService.login()
   - 사용자 조회
   - 비밀번호 검증
   - JWT 토큰 생성

3. 토큰 저장
   Set-Cookie: access_token=xxx; HttpOnly; Secure

4. 인증된 요청
   Cookie: access_token=xxx
   → get_current_user()
   → User 객체 반환
```

### 5.2 CRUD 흐름

```
1. 생성 요청
   POST /partials/items
   Form: {title, description}

2. 서비스 처리
   ItemService.create(item_in, owner)
   - Model 생성
   - DB 저장

3. 응답
   HTML 파셜 + HX-Trigger: showToast

4. 클라이언트
   - DOM 업데이트
   - 토스트 표시
```

## 6. 인증 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                    Authentication Flow                    │
│                                                          │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐            │
│  │ Client  │────▶│ FastAPI │────▶│AuthServ │            │
│  │(Browser)│     │ Router  │     │         │            │
│  └─────────┘     └─────────┘     └─────────┘            │
│       ▲               │               │                  │
│       │               ▼               ▼                  │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐            │
│  │ Cookie  │◀────│   JWT   │◀────│UserServ │            │
│  │(httpOnly)│    │ Token   │     │         │            │
│  └─────────┘     └─────────┘     └─────────┘            │
└──────────────────────────────────────────────────────────┘
```

## 7. 템플릿 렌더링 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                  Template Rendering                       │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │                    base.html                         ││
│  │  ┌─────────────────────────────────────────────────┐││
│  │  │                  navbar.html                     │││
│  │  └─────────────────────────────────────────────────┘││
│  │  ┌─────────────────────────────────────────────────┐││
│  │  │              {% block content %}                 │││
│  │  │                                                  │││
│  │  │  ┌─────────────────────────────────────────────┐│││
│  │  │  │        page.html (extends base)             ││││
│  │  │  │                                              ││││
│  │  │  │  ┌─────────────────────────────────────────┐││││
│  │  │  │  │     partial.html (HTMX Target)          │││││
│  │  │  │  └─────────────────────────────────────────┘││││
│  │  │  └─────────────────────────────────────────────┘│││
│  │  │                                                  │││
│  │  └─────────────────────────────────────────────────┘││
│  │  ┌─────────────────────────────────────────────────┐││
│  │  │                  footer.html                     │││
│  │  └─────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

## 8. 확장 가이드

### 8.1 새 기능 추가

1. **모델 추가**: `app/models/new_feature.py`
2. **스키마 추가**: `app/schemas/new_feature.py`
3. **서비스 추가**: `app/services/new_feature.py`
4. **API 추가**: `app/api/v1/new_feature.py`
5. **파셜 추가**: `app/partials/new_feature.py`
6. **템플릿 추가**: `templates/partials/new_feature/`

### 8.2 마이크로서비스 분리

이 구조는 마이크로서비스 분리에 적합합니다:
- 각 서비스 레이어가 독립적
- 명확한 API 경계
- 데이터베이스 모델 분리 용이
