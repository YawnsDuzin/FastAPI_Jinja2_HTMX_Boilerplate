# 빠른 시작 가이드

## 1. 요구 사항

- Python 3.11 이상
- pip 또는 poetry
- Git
- (선택) Docker & Docker Compose

## 2. 설치

### 2.1 저장소 클론

```bash
git clone <repository-url>
cd fastapi-htmx-boilerplate
```

### 2.2 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 활성화 (Linux/macOS)
source venv/bin/activate

# 활성화 (Windows)
venv\Scripts\activate
```

### 2.3 의존성 설치

```bash
# 프로덕션 의존성만
pip install -r requirements.txt

# 개발 의존성 포함
pip install -r requirements-dev.txt
```

### 2.4 환경 변수 설정

```bash
# 환경 변수 파일 복사
cp .env.example .env

# .env 파일 편집
# SECRET_KEY와 JWT_SECRET_KEY를 안전한 값으로 변경
```

주요 환경 변수:

```env
APP_NAME=FastAPI-HTMX-Boilerplate
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-change-me
DATABASE_URL=sqlite+aiosqlite:///./app.db
JWT_SECRET_KEY=your-jwt-secret-change-me
```

## 3. 데이터베이스 설정

### 3.1 SQLite (기본)

SQLite는 별도 설정 없이 바로 사용 가능합니다.

```bash
# 마이그레이션 실행
alembic upgrade head
```

### 3.2 PostgreSQL (선택)

```bash
# PostgreSQL 연결 설정 (.env 수정)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# 마이그레이션 실행
alembic upgrade head
```

## 4. 개발 서버 실행

```bash
# 개발 서버 실행 (자동 리로드)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 또는 간단히
python -m uvicorn app.main:app --reload
```

서버가 실행되면:
- 애플리케이션: http://localhost:8001
- API 문서: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 5. Docker 실행

### 5.1 기본 실행

```bash
# 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 5.2 개발 모드

```bash
# 개발 모드로 실행 (핫 리로드)
docker-compose --profile dev up
```

### 5.3 PostgreSQL과 함께 실행

```bash
# PostgreSQL 프로필 포함
docker-compose --profile postgres up -d
```

## 6. 첫 사용자 생성

### 6.1 웹 인터페이스

1. http://localhost:8001/register 접속
2. 이메일, 사용자명, 비밀번호 입력
3. 회원가입 완료 후 로그인

### 6.2 API 사용

```bash
# 회원가입
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "testuser", "password": "password123"}'

# 로그인
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

## 7. 프로젝트 탐색

### 7.1 주요 페이지

| URL | 설명 |
|-----|------|
| `/` | 홈페이지 |
| `/about` | 소개 페이지 |
| `/login` | 로그인 |
| `/register` | 회원가입 |
| `/dashboard` | 대시보드 (로그인 필요) |
| `/items` | 아이템 관리 (로그인 필요) |
| `/profile` | 프로필 설정 (로그인 필요) |

### 7.2 API 엔드포인트

| 메서드 | URL | 설명 |
|--------|-----|------|
| POST | `/api/v1/auth/register` | 회원가입 |
| POST | `/api/v1/auth/login` | 로그인 |
| POST | `/api/v1/auth/logout` | 로그아웃 |
| GET | `/api/v1/auth/me` | 현재 사용자 |
| GET | `/api/v1/items` | 아이템 목록 |
| POST | `/api/v1/items` | 아이템 생성 |
| GET | `/api/v1/items/{id}` | 아이템 조회 |
| PATCH | `/api/v1/items/{id}` | 아이템 수정 |
| DELETE | `/api/v1/items/{id}` | 아이템 삭제 |

## 8. 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=app

# 특정 테스트
pytest tests/test_api/test_auth.py -v
```

## 9. 코드 품질 도구

```bash
# 코드 포맷팅
black app tests
isort app tests

# 린트 검사
ruff check app tests

# 타입 검사
mypy app
```

## 10. 다음 단계

1. [프로젝트 구조](./09-directory-structure.md) 이해하기
2. [FastAPI 가이드](./03-fastapi-guide.md) 읽기
3. [HTMX 가이드](./05-htmx-guide.md)로 동적 UI 구현
4. 새 기능 추가하기

## 11. 문제 해결

### 포트 충돌
```bash
# 8001 포트 사용 중인 프로세스 확인
lsof -i :8001

# 다른 포트로 실행
uvicorn app.main:app --reload --port 8001
```

### 데이터베이스 초기화
```bash
# 데이터베이스 삭제 후 재생성
rm app.db
alembic upgrade head
```

### 의존성 문제
```bash
# 캐시 정리 후 재설치
pip cache purge
pip install -r requirements.txt --no-cache-dir
```
