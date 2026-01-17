# 프로젝트 개요

## 1. 프로젝트 소개

FastAPI + Jinja2 + HTMX 보일러플레이트는 모던 풀스택 웹 애플리케이션을 빠르게 개발할 수 있는 기반 코드입니다. JavaScript 프레임워크 없이 동적인 SPA-like 경험을 제공합니다.

### 이 보일러플레이트를 사용하면

- ✅ **빠른 프로토타이핑**: 복잡한 빌드 설정 없이 바로 개발 시작
- ✅ **낮은 학습 곡선**: React/Vue 없이 Python + HTML만으로 동적 웹앱 구현
- ✅ **SEO 친화적**: 서버사이드 렌더링으로 검색엔진 최적화
- ✅ **유지보수 용이**: 서버 중심 아키텍처로 코드 관리 단순화

### 핵심 철학

| 원칙 | 설명 | 장점 |
|------|------|------|
| **제로 JavaScript 빌드** | npm, webpack, vite 등의 빌드 도구 없이 개발 | 복잡한 프론트엔드 툴체인 불필요 |
| **서버사이드 렌더링 우선** | HTML을 서버에서 생성하여 클라이언트에 전달 | SEO 친화적, 빠른 초기 로딩 |
| **점진적 향상** | 기본 HTML 동작 위에 HTMX로 동적 기능 추가 | JavaScript 비활성화 시에도 기본 동작 |
| **단순함** | 복잡한 상태 관리 없이 직관적인 개발 | 디버깅 용이, 빠른 개발 |

## 2. 기술 스택 상세

### 2.1 백엔드

| 기술 | 버전 | 역할 | 특징 |
|------|------|------|------|
| **FastAPI** | 0.115+ | 웹 프레임워크 | 비동기 지원, 자동 API 문서화, 타입 검증 |
| **SQLAlchemy** | 2.0+ | ORM | 비동기 DB 지원, 타입 힌트, 마이그레이션 |
| **Pydantic** | 2.0+ | 데이터 검증 | 런타임 타입 검증, 직렬화/역직렬화 |
| **python-jose** | 3.3+ | JWT 인증 | 토큰 생성/검증, 암호화 |
| **passlib** | 1.7+ | 비밀번호 해싱 | bcrypt 알고리즘, 안전한 해싱 |
| **aiosqlite** | 0.19+ | SQLite 비동기 | 개발용 경량 DB |
| **asyncpg** | 0.29+ | PostgreSQL 비동기 | 프로덕션용 고성능 DB |

### 2.2 프론트엔드

| 기술 | 버전 | 역할 | 특징 |
|------|------|------|------|
| **Jinja2** | 3.1+ | 템플릿 엔진 | 상속, 매크로, 필터, 자동 XSS 방지 |
| **HTMX** | 2.0+ | 동적 UI | HTML 속성으로 AJAX 구현, 서버 중심 |
| **Alpine.js** | 3.x | 클라이언트 상호작용 | 모달, 드롭다운 등 UI 상태 관리 |
| **TailwindCSS** | 3.4+ | 스타일링 | 유틸리티 기반 CSS, 빠른 스타일링 |

### 2.3 개발 도구

| 도구 | 용도 | 설명 |
|------|------|------|
| **Alembic** | DB 마이그레이션 | SQLAlchemy 모델 변경 시 스키마 동기화 |
| **pytest** | 테스팅 | 비동기 테스트 지원, 픽스처, 커버리지 |
| **Black** | 코드 포맷팅 | Python 코드 자동 포맷팅 |
| **Ruff** | 린팅 | 빠른 Python 린터 |
| **mypy** | 타입 검사 | 정적 타입 검사 |

## 3. 주요 기능

### 3.1 인증 시스템

완전한 JWT 기반 인증 시스템이 구현되어 있습니다.

```
┌─────────────────────────────────────────────────────────────┐
│                      인증 흐름                               │
├─────────────────────────────────────────────────────────────┤
│  1. 사용자 → 로그인 폼 제출 (이메일, 비밀번호)                │
│  2. 서버 → 비밀번호 검증 → JWT 토큰 생성                     │
│  3. 서버 → httpOnly 쿠키에 토큰 저장                        │
│  4. 이후 요청 → 쿠키의 토큰으로 자동 인증                    │
│  5. 로그아웃 → 쿠키 삭제                                    │
└─────────────────────────────────────────────────────────────┘
```

**구현된 기능:**
- 회원가입 (이메일 중복 검사, 비밀번호 해싱)
- 로그인/로그아웃
- 비밀번호 변경
- 프로필 수정
- 세션 관리 (JWT 만료 시간)

### 3.2 CRUD 샘플 (아이템)

완전한 CRUD 예제가 포함되어 있어 새 기능 추가 시 참고할 수 있습니다.

| 기능 | API 엔드포인트 | HTMX 파셜 | 설명 |
|------|---------------|-----------|------|
| 목록 조회 | `GET /api/v1/items` | `/partials/items` | 페이지네이션, 검색 |
| 상세 조회 | `GET /api/v1/items/{id}` | `/partials/items/{id}` | 단일 아이템 |
| 생성 | `POST /api/v1/items` | `/partials/items` | 모달 폼 |
| 수정 | `PATCH /api/v1/items/{id}` | `/partials/items/{id}` | 인라인 수정 |
| 삭제 | `DELETE /api/v1/items/{id}` | `/partials/items/{id}` | 확인 모달 |

### 3.3 UI 컴포넌트

재사용 가능한 UI 컴포넌트가 준비되어 있습니다.

| 컴포넌트 | 위치 | 설명 |
|----------|------|------|
| 네비게이션 바 | `components/navbar.html` | 반응형, 모바일 메뉴 |
| 모달 | `components/modal.html` | Alpine.js 기반, 애니메이션 |
| 토스트 알림 | `components/toast.html` | 자동 사라짐, 다양한 타입 |
| 폼 컴포넌트 | `components/form/` | 입력, 선택, 체크박스 등 |
| 테이블 | `components/table.html` | 정렬, 페이지네이션 |

### 3.4 다크 모드

시스템 설정 감지 및 수동 토글이 가능한 다크 모드가 구현되어 있습니다.

```javascript
// 다크 모드 감지 (Alpine.js)
x-data="{
    dark: localStorage.getItem('darkMode') === 'true'
          || (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches)
}"
```

## 4. 프로젝트 구조 개요

```
fastapi-htmx-boilerplate/
│
├── app/                    # 🔷 애플리케이션 메인 코드
│   ├── api/               # REST API (JSON 응답)
│   │   ├── deps.py        # 의존성 주입 (인증, DB)
│   │   └── v1/            # API 버전 1
│   ├── pages/             # HTML 페이지 라우터
│   ├── partials/          # HTMX 파셜 라우터
│   ├── models/            # SQLAlchemy 모델 (DB 테이블)
│   ├── schemas/           # Pydantic 스키마 (요청/응답)
│   ├── services/          # 비즈니스 로직
│   └── core/              # 핵심 유틸리티 (보안, 예외)
│
├── templates/             # 🔷 Jinja2 템플릿
│   ├── base.html          # 기본 레이아웃
│   ├── components/        # 재사용 컴포넌트
│   ├── pages/             # 전체 페이지
│   └── partials/          # HTMX 파셜 (HTML 조각)
│
├── static/                # 🔷 정적 파일 (CSS, JS, 이미지)
├── tests/                 # 🔷 테스트 코드
├── alembic/               # 🔷 DB 마이그레이션
└── docs/                  # 🔷 문서
```

## 5. 3가지 라우터 레이어 이해하기

이 보일러플레이트의 핵심 개념은 **3가지 라우터 레이어**입니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                        3가지 라우터 레이어                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ API Layer (/api/v1/*)                                       │
│     └─ JSON 데이터 반환                                          │
│     └─ 모바일 앱, 외부 서비스 연동용                               │
│     └─ 예: GET /api/v1/items → JSON 배열                        │
│                                                                 │
│  2️⃣ Pages Layer (/*)                                            │
│     └─ 전체 HTML 페이지 반환                                      │
│     └─ base.html을 상속하는 완전한 페이지                         │
│     └─ 예: GET /dashboard → 전체 대시보드 페이지                  │
│                                                                 │
│  3️⃣ Partials Layer (/partials/*)                                │
│     └─ HTML 조각 반환 (HTMX용)                                   │
│     └─ 페이지 일부분만 동적 업데이트                               │
│     └─ 예: GET /partials/items → 아이템 목록 HTML만              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 왜 3가지로 나누었나?

| 레이어 | 사용 시점 | 장점 |
|--------|----------|------|
| **API** | 외부 연동, 모바일 앱 | 표준 REST API, 재사용성 |
| **Pages** | 첫 페이지 로드, SEO | 완전한 HTML, 검색엔진 인덱싱 |
| **Partials** | 페이지 내 동적 업데이트 | 빠른 응답, 부분 렌더링 |

## 6. 왜 이 스택인가?

### 6.1 HTMX를 선택한 이유

| 기존 방식 (React/Vue) | HTMX 방식 |
|----------------------|-----------|
| JSON API 호출 → 클라이언트에서 HTML 생성 | 서버에서 HTML 생성 → 그대로 삽입 |
| 복잡한 상태 관리 (Redux, Vuex) | 서버가 상태 관리 |
| JavaScript 번들 크기 증가 | 14KB 경량 라이브러리 |
| SEO 어려움 (SSR 필요) | 기본적으로 SSR |

```html
<!-- HTMX: HTML 속성만으로 동적 기능 -->
<button hx-get="/partials/items"
        hx-target="#item-list"
        hx-swap="innerHTML">
    새로고침
</button>
```

### 6.2 FastAPI를 선택한 이유

```python
# 타입 힌트로 자동 검증 + 자동 문서화
@app.post("/items")
async def create_item(item: ItemCreate) -> ItemResponse:
    # Pydantic이 자동으로 검증
    # Swagger UI에 자동 문서화
    return await item_service.create(item)
```

- **비동기 기본 지원**: async/await로 높은 동시성 처리
- **타입 안전**: 런타임 타입 검증, IDE 자동완성
- **자동 문서화**: OpenAPI/Swagger 자동 생성
- **의존성 주입**: 깔끔한 코드 구조

### 6.3 Jinja2를 선택한 이유

```jinja2
{# 템플릿 상속으로 코드 재사용 #}
{% extends "base.html" %}

{% block content %}
    {# 반복문, 조건문 지원 #}
    {% for item in items %}
        {% include "partials/items/item.html" %}
    {% endfor %}
{% endblock %}
```

- **Python 친화적**: Python 개발자에게 익숙한 문법
- **보안**: 자동 XSS 방지 (HTML 이스케이프)
- **성능**: 컴파일된 템플릿
- **확장성**: 커스텀 필터, 함수 추가 용이

## 7. 사용 사례

### ✅ 적합한 프로젝트

| 유형 | 이유 |
|------|------|
| **관리자 대시보드** | CRUD 중심, 빠른 개발 |
| **내부 도구** | 복잡한 빌드 불필요, 빠른 배포 |
| **MVP/프로토타입** | 빠른 검증, 나중에 확장 가능 |
| **콘텐츠 관리 시스템** | SEO 중요, 서버 렌더링 |
| **폼 중심 애플리케이션** | 서버 검증, 동적 폼 |
| **전자상거래 (기본)** | 상품 목록, 장바구니, 주문 |

### ❌ 다른 스택 권장

| 유형 | 권장 스택 | 이유 |
|------|----------|------|
| **실시간 협업 앱** | React + WebSocket | 복잡한 클라이언트 상태 |
| **복잡한 대화형 UI** | React/Vue | 많은 클라이언트 로직 |
| **오프라인 지원 앱** | PWA (React/Vue) | Service Worker 필요 |
| **모바일 앱** | React Native, Flutter | 네이티브 경험 |
| **게임/캔버스 앱** | 전용 게임 엔진 | 복잡한 렌더링 |

## 8. 학습 로드맵

### 초급 (1-2일)

1. [빠른 시작 가이드](./02-quick-start.md) - 프로젝트 실행
2. 기본 페이지 탐색 (`/`, `/login`, `/dashboard`)
3. API 문서 확인 (`/docs`)

### 중급 (3-5일)

4. [FastAPI 가이드](./03-fastapi-guide.md) - 라우터, 의존성 주입
5. [HTMX 가이드](./05-htmx-guide.md) - 동적 UI 패턴
6. [Jinja2 가이드](./04-jinja2-guide.md) - 템플릿 문법
7. 아이템 CRUD 코드 분석

### 고급 (1주+)

8. [아키텍처 문서](./08-architecture.md) - 시스템 구조 이해
9. [SQLAlchemy 가이드](./07-sqlalchemy-guide.md) - 데이터베이스 작업
10. 새 기능 직접 추가해보기
11. 테스트 코드 작성

## 9. 다음 단계

- 🚀 **지금 바로 시작하기**: [빠른 시작 가이드](./02-quick-start.md)
- 📚 **기술 스택 학습**: [FastAPI 가이드](./03-fastapi-guide.md)
- 🏗️ **구조 이해하기**: [아키텍처 문서](./08-architecture.md)
