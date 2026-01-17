# FastAPI + Jinja2 + HTMX 보일러플레이트 문서

이 문서는 FastAPI + Jinja2 + HTMX 보일러플레이트의 상세 가이드를 제공합니다.

## 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/YawnsDuzin/FastAPI_Jinja2_HTMX_Boilerplate.git
cd FastAPI_Jinja2_HTMX_Boilerplate

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp .env.example .env

# 5. 데이터베이스 마이그레이션
alembic upgrade head

# 6. 개발 서버 실행
python run.py
```

브라우저에서 http://localhost:8001 접속

---

## 문서 구조

### 1. 시작하기

| 문서 | 설명 | 대상 |
|------|------|------|
| [프로젝트 소개](./01-project-overview.md) | 프로젝트 목적, 특징, 기술 스택 | 모든 사용자 |
| [빠른 시작 가이드](./02-quick-start.md) | OS별 설치 및 실행 방법 | 초급자 |

### 2. 기술 스택 가이드

| 문서 | 설명 | 분량 |
|------|------|------|
| [FastAPI 가이드](./03-fastapi-guide.md) | FastAPI 문법, 라우터, 의존성 주입 | 상세 |
| [Jinja2 가이드](./04-jinja2-guide.md) | Jinja2 템플릿 문법, 상속, 필터 | 상세 |
| [HTMX 가이드](./05-htmx-guide.md) | HTMX 속성, 패턴, 서버 연동 | 상세 |
| [Alpine.js 가이드](./06-alpinejs-guide.md) | Alpine.js 기본 사용법, 상태 관리 | 상세 |
| [SQLAlchemy 가이드](./07-sqlalchemy-guide.md) | SQLAlchemy 2.0, 비동기 ORM | 상세 |

### 3. 프로젝트 구조

| 문서 | 설명 |
|------|------|
| [아키텍처 설명](./08-architecture.md) | 시스템 아키텍처, 계층 구조, 데이터 흐름 |
| [디렉토리 구조](./09-directory-structure.md) | 파일/폴더별 역할, 명명 규칙 |

### 4. 개발 가이드

| 문서 | 설명 |
|------|------|
| [개발 환경 설정](./10-development-setup.md) | IDE 설정, 코드 품질 도구, OS별 설정 |
| [테스트 가이드](./11-testing-guide.md) | pytest, 테스트 작성법, 커버리지 |
| [배포 가이드](./12-deployment-guide.md) | Docker, 프로덕션 설정, CI/CD |

### 5. API 레퍼런스

| 문서 | 설명 |
|------|------|
| [API 엔드포인트](./13-api-reference.md) | 모든 API 엔드포인트, 요청/응답 형식 |

---

## 핵심 개념

### 3가지 라우터 레이어

이 보일러플레이트는 용도에 따라 3가지 라우터 레이어를 사용합니다.

| 레이어 | 경로 | 응답 | 용도 |
|--------|------|------|------|
| **API** | `/api/v1/*` | JSON | 외부 연동, 모바일 앱 |
| **Pages** | `/*` | 전체 HTML | 첫 페이지 로드, SEO |
| **Partials** | `/partials/*` | HTML 조각 | HTMX 부분 업데이트 |

```
브라우저 → GET /dashboard → Pages Layer → 전체 HTML 페이지
HTMX    → GET /partials/items → Partials Layer → HTML 조각만
Mobile  → GET /api/v1/items → API Layer → JSON 데이터
```

### 요청 흐름

```
Router (HTTP 요청 처리)
  ↓ Depends()
Dependencies (인증, DB 세션)
  ↓
Service (비즈니스 로직)
  ↓
Model (SQLAlchemy ORM)
  ↓
Database (SQLite/PostgreSQL)
```

---

## 학습 로드맵

### 초급 (1-2일)

1. [빠른 시작 가이드](./02-quick-start.md) - 프로젝트 실행
2. 기본 페이지 탐색 (`/`, `/login`, `/dashboard`)
3. API 문서 확인 (`http://localhost:8001/docs`)

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

---

## OS별 설치 요약

### Windows

```powershell
# Python 설치 (winget)
winget install Python.Python.3.12

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 실행 정책 오류 시
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS

```bash
# Python 설치 (Homebrew)
brew install python@3.12

# 가상환경 활성화
source venv/bin/activate
```

### Linux (Ubuntu)

```bash
# Python 설치
sudo apt install python3.12 python3.12-venv

# 가상환경 활성화
source venv/bin/activate
```

### 라즈베리파이

```bash
# pyenv로 Python 설치 권장
pyenv install 3.12.0
pyenv global 3.12.0

# 가상환경 활성화
source venv/bin/activate
```

자세한 내용은 [빠른 시작 가이드](./02-quick-start.md)를 참조하세요.

---

## 자주 사용하는 명령어

### 개발 서버

```bash
# 개발 서버 실행 (포트 8001)
python run.py

# 또는
uvicorn app.main:app --reload --port 8001
```

### 데이터베이스

```bash
# 마이그레이션 적용
alembic upgrade head

# 새 마이그레이션 생성
alembic revision --autogenerate -m "설명"
```

### 테스트

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=app
```

### 코드 품질

```bash
# 포맷팅
black app tests
isort app tests

# 린트
ruff check app tests

# 타입 검사
mypy app
```

---

## 주요 URL

| URL | 설명 |
|-----|------|
| http://localhost:8001 | 메인 애플리케이션 |
| http://localhost:8001/docs | Swagger API 문서 |
| http://localhost:8001/redoc | ReDoc API 문서 |
| http://localhost:8001/login | 로그인 페이지 |
| http://localhost:8001/register | 회원가입 페이지 |
| http://localhost:8001/dashboard | 대시보드 (인증 필요) |

---

## 기여하기

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다.

1. 저장소 Fork
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경 사항 커밋 (`git commit -m 'feat: Add amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

---

## 라이선스

MIT License
