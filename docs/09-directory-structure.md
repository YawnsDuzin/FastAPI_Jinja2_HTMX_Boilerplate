# 디렉토리 구조

## 전체 프로젝트 구조

```
fastapi-htmx-boilerplate/
│
├── app/                        # 애플리케이션 메인 패키지
│   ├── __init__.py            # 패키지 초기화, 버전 정보
│   ├── main.py                # FastAPI 앱 엔트리포인트
│   ├── config.py              # 환경 설정 (Pydantic Settings)
│   ├── database.py            # DB 연결 설정
│   │
│   ├── api/                   # REST API 라우터
│   │   ├── __init__.py
│   │   ├── deps.py            # 공통 의존성 (인증, DB 세션)
│   │   └── v1/                # API 버전 1
│   │       ├── __init__.py
│   │       ├── router.py      # 라우터 통합
│   │       ├── auth.py        # 인증 엔드포인트
│   │       ├── users.py       # 사용자 엔드포인트
│   │       └── items.py       # 아이템 엔드포인트
│   │
│   ├── pages/                 # HTML 페이지 라우터
│   │   ├── __init__.py
│   │   ├── router.py          # 페이지 라우터 통합
│   │   ├── home.py            # 홈, 소개 페이지
│   │   ├── auth.py            # 로그인/회원가입 페이지
│   │   └── dashboard.py       # 대시보드, 아이템 페이지
│   │
│   ├── partials/              # HTMX 파셜 라우터
│   │   ├── __init__.py
│   │   ├── router.py          # 파셜 라우터 통합
│   │   ├── items.py           # 아이템 CRUD 파셜
│   │   ├── modals.py          # 모달 파셜
│   │   └── toasts.py          # 토스트 알림 파셜
│   │
│   ├── models/                # SQLAlchemy 모델
│   │   ├── __init__.py        # 모델 export
│   │   ├── base.py            # 베이스 모델, 믹스인
│   │   ├── user.py            # 사용자 모델
│   │   └── item.py            # 아이템 모델
│   │
│   ├── schemas/               # Pydantic 스키마
│   │   ├── __init__.py        # 스키마 export
│   │   ├── common.py          # 공통 스키마
│   │   ├── user.py            # 사용자 스키마
│   │   └── item.py            # 아이템 스키마
│   │
│   ├── services/              # 비즈니스 로직
│   │   ├── __init__.py        # 서비스 export
│   │   ├── auth.py            # 인증 서비스
│   │   ├── user.py            # 사용자 서비스
│   │   └── item.py            # 아이템 서비스
│   │
│   └── core/                  # 핵심 유틸리티
│       ├── __init__.py
│       ├── security.py        # JWT, 비밀번호 해싱
│       ├── exceptions.py      # 커스텀 예외
│       └── templates.py       # Jinja2 설정
│
├── templates/                 # Jinja2 템플릿
│   ├── base.html             # 기본 레이아웃
│   │
│   ├── components/           # 재사용 컴포넌트
│   │   ├── navbar.html       # 네비게이션 바
│   │   ├── sidebar.html      # 사이드바
│   │   ├── footer.html       # 푸터
│   │   ├── modal.html        # 모달 컴포넌트
│   │   └── toast.html        # 토스트 컴포넌트
│   │
│   ├── pages/                # 전체 페이지 템플릿
│   │   ├── home.html         # 홈페이지
│   │   ├── about.html        # 소개 페이지
│   │   ├── login.html        # 로그인
│   │   ├── register.html     # 회원가입
│   │   ├── dashboard.html    # 대시보드
│   │   ├── items.html        # 아이템 목록
│   │   ├── profile.html      # 프로필
│   │   ├── settings.html     # 설정
│   │   ├── 404.html          # 404 에러 페이지
│   │   └── 500.html          # 500 에러 페이지
│   │
│   └── partials/             # HTMX 파셜 템플릿
│       ├── items/
│       │   ├── list.html     # 아이템 목록
│       │   ├── item.html     # 단일 아이템
│       │   ├── form.html     # 생성/수정 폼
│       │   └── empty.html    # 빈 상태
│       ├── modals/
│       │   ├── confirm.html  # 확인 모달
│       │   ├── alert.html    # 알림 모달
│       │   └── form.html     # 폼 모달
│       └── toasts/
│           ├── success.html  # 성공 토스트
│           ├── error.html    # 에러 토스트
│           ├── info.html     # 정보 토스트
│           └── warning.html  # 경고 토스트
│
├── static/                   # 정적 파일
│   ├── css/
│   │   └── custom.css       # 커스텀 스타일
│   ├── js/
│   │   └── app.js           # 앱 JavaScript
│   └── img/                 # 이미지
│
├── tests/                   # 테스트
│   ├── __init__.py
│   ├── conftest.py          # 테스트 설정, 픽스처
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_auth.py     # 인증 API 테스트
│   │   └── test_items.py    # 아이템 API 테스트
│   └── test_pages/
│       ├── __init__.py
│       └── test_home.py     # 페이지 테스트
│
├── alembic/                 # DB 마이그레이션
│   ├── env.py               # Alembic 환경 설정
│   ├── script.py.mako       # 마이그레이션 템플릿
│   └── versions/            # 마이그레이션 파일들
│
├── docs/                    # 문서
│   ├── README.md            # 문서 인덱스
│   ├── 01-project-overview.md
│   ├── 02-quick-start.md
│   └── ...
│
├── .env.example             # 환경변수 예시
├── .gitignore               # Git 무시 파일
├── .dockerignore            # Docker 무시 파일
├── alembic.ini              # Alembic 설정
├── Dockerfile               # Docker 이미지 빌드
├── docker-compose.yml       # Docker Compose 설정
├── requirements.txt         # 프로덕션 의존성
├── requirements-dev.txt     # 개발 의존성
└── README.md                # 프로젝트 README
```

## 파일별 설명

### 애플리케이션 코어

| 파일 | 설명 |
|------|------|
| `app/main.py` | FastAPI 앱 인스턴스 생성, 라우터 등록, 미들웨어 설정 |
| `app/config.py` | 환경 변수 기반 설정 관리 (Pydantic Settings) |
| `app/database.py` | SQLAlchemy 엔진, 세션 설정, 의존성 |

### API 관련

| 파일 | 설명 |
|------|------|
| `app/api/deps.py` | 공통 의존성 (인증, DB 세션) |
| `app/api/v1/auth.py` | 회원가입, 로그인, 로그아웃 API |
| `app/api/v1/users.py` | 사용자 CRUD API |
| `app/api/v1/items.py` | 아이템 CRUD API |

### 페이지 관련

| 파일 | 설명 |
|------|------|
| `app/pages/home.py` | 홈, 소개 페이지 렌더링 |
| `app/pages/auth.py` | 로그인, 회원가입 페이지 렌더링 |
| `app/pages/dashboard.py` | 대시보드, 아이템 페이지 렌더링 |

### 파셜 관련

| 파일 | 설명 |
|------|------|
| `app/partials/items.py` | 아이템 CRUD HTMX 파셜 |
| `app/partials/modals.py` | 모달 파셜 |
| `app/partials/toasts.py` | 토스트 알림 파셜 |

### 모델 & 스키마

| 파일 | 설명 |
|------|------|
| `app/models/base.py` | BaseModel, TimestampMixin |
| `app/models/user.py` | User 모델 (인증, 프로필) |
| `app/models/item.py` | Item 모델 (CRUD 예제) |
| `app/schemas/user.py` | 사용자 요청/응답 스키마 |
| `app/schemas/item.py` | 아이템 요청/응답 스키마 |

### 서비스

| 파일 | 설명 |
|------|------|
| `app/services/auth.py` | 인증 비즈니스 로직 |
| `app/services/user.py` | 사용자 CRUD 로직 |
| `app/services/item.py` | 아이템 CRUD 로직 |

### 핵심 유틸리티

| 파일 | 설명 |
|------|------|
| `app/core/security.py` | JWT 생성/검증, 비밀번호 해싱 |
| `app/core/exceptions.py` | 커스텀 예외, 예외 핸들러 |
| `app/core/templates.py` | Jinja2 설정, 커스텀 필터 |

## 명명 규칙

### 파일 명명

- **Python 파일**: snake_case (`user_service.py`)
- **템플릿 파일**: kebab-case 또는 snake_case (`forgot-password.html`)
- **정적 파일**: kebab-case (`custom.css`)

### 클래스 명명

- **모델**: PascalCase 단수형 (`User`, `Item`)
- **스키마**: PascalCase + 동작 (`UserCreate`, `ItemUpdate`)
- **서비스**: PascalCase + Service (`AuthService`, `ItemService`)

### 함수 명명

- **라우터**: 동사_목적어 (`get_items`, `create_item`)
- **서비스**: 동사_목적어 (`get_by_id`, `create`)
