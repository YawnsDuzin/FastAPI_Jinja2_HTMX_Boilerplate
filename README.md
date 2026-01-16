# FastAPI + Jinja2 + HTMX 보일러플레이트

JavaScript 프레임워크 없이 동적인 SPA-like 경험을 제공하는 모던 풀스택 웹 애플리케이션 보일러플레이트입니다.

## 기술 스택

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| Backend | FastAPI | 0.115+ | 비동기 웹 프레임워크 |
| Template | Jinja2 | 3.1+ | 서버사이드 렌더링 |
| Frontend | HTMX | 2.0+ | AJAX/동적 UI |
| UI | Alpine.js | 3.x | 클라이언트 상호작용 |
| CSS | TailwindCSS | 3.4+ | 스타일링 (CDN) |
| Database | SQLAlchemy | 2.0+ | 비동기 ORM |
| Auth | python-jose | 3.3+ | JWT 인증 |

## 주요 기능

- JWT 기반 인증 시스템 (httpOnly 쿠키)
- HTMX를 활용한 동적 CRUD
- 다크 모드 지원
- 반응형 디자인
- 토스트 알림
- 모달 다이얼로그
- 페이지네이션
- 검색 기능

## 빠른 시작

### 로컬 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env

# 데이터베이스 마이그레이션
alembic upgrade head

# 개발 서버 실행
uvicorn app.main:app --reload
```

### Docker 실행

```bash
# 빌드 및 실행
docker-compose up -d

# 개발 모드
docker-compose --profile dev up
```

## 프로젝트 구조

```
├── app/
│   ├── api/v1/          # REST API 라우터
│   ├── pages/           # HTML 페이지 라우터
│   ├── partials/        # HTMX 파셜 라우터
│   ├── models/          # SQLAlchemy 모델
│   ├── schemas/         # Pydantic 스키마
│   ├── services/        # 비즈니스 로직
│   └── core/            # 핵심 유틸리티
├── templates/           # Jinja2 템플릿
├── static/              # 정적 파일
├── tests/               # 테스트
├── alembic/             # DB 마이그레이션
└── docs/                # 문서
```

## 문서

상세한 문서는 [docs/](./docs/) 폴더를 참조하세요.

- [프로젝트 개요](./docs/01-project-overview.md)
- [빠른 시작 가이드](./docs/02-quick-start.md)
- [FastAPI 가이드](./docs/03-fastapi-guide.md)
- [Jinja2 가이드](./docs/04-jinja2-guide.md)
- [HTMX 가이드](./docs/05-htmx-guide.md)
- [Alpine.js 가이드](./docs/06-alpinejs-guide.md)
- [SQLAlchemy 가이드](./docs/07-sqlalchemy-guide.md)
- [아키텍처 설명](./docs/08-architecture.md)
- [디렉토리 구조](./docs/09-directory-structure.md)
- [개발 환경 설정](./docs/10-development-setup.md)
- [API 레퍼런스](./docs/13-api-reference.md)

## API 엔드포인트

### 인증
| 메서드 | URL | 설명 |
|--------|-----|------|
| POST | `/api/v1/auth/register` | 회원가입 |
| POST | `/api/v1/auth/login` | 로그인 |
| POST | `/api/v1/auth/logout` | 로그아웃 |
| GET | `/api/v1/auth/me` | 현재 사용자 |

### 아이템
| 메서드 | URL | 설명 |
|--------|-----|------|
| GET | `/api/v1/items` | 목록 조회 |
| POST | `/api/v1/items` | 생성 |
| GET | `/api/v1/items/{id}` | 상세 조회 |
| PATCH | `/api/v1/items/{id}` | 수정 |
| DELETE | `/api/v1/items/{id}` | 삭제 |

## 환경 변수

```env
APP_NAME=FastAPI-HTMX-Boilerplate
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite+aiosqlite:///./app.db
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 테스트

```bash
# 전체 테스트
pytest

# 커버리지
pytest --cov=app
```

## 라이선스

MIT License
