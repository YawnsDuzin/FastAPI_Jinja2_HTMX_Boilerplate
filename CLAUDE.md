# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 개발 명령어

```bash
# 개발 서버 실행 (포트 8001)
python run.py
# 또는
uvicorn app.main:app --reload --port 8001

# 테스트
pytest                              # 전체 테스트
pytest tests/test_api/test_auth.py  # 특정 파일
pytest -k "test_login"              # 특정 테스트
pytest --cov=app                    # 커버리지

# 코드 품질
black app tests                     # 포맷팅
isort app tests                     # import 정렬
ruff check app tests                # 린트
mypy app                            # 타입 검사

# 데이터베이스
alembic upgrade head                # 마이그레이션 적용
alembic revision --autogenerate -m "설명"  # 마이그레이션 생성
```

## 아키텍처 개요

FastAPI + Jinja2 + HTMX 기반의 풀스택 보일러플레이트. JavaScript 프레임워크 없이 동적 SPA-like 경험 제공.

### 3가지 라우터 레이어

| 레이어 | 경로 | 용도 | 응답 |
|--------|------|------|------|
| API | `/api/v1/*` | REST API | JSON |
| Pages | `/*` | 전체 페이지 | HTML (base.html 상속) |
| Partials | `/partials/*` | HTMX 부분 업데이트 | HTML 조각 |

### 요청 흐름

```
Router (app/api/, app/pages/, app/partials/)
  ↓ Depends()
Service (app/services/) - 비즈니스 로직
  ↓
Model (app/models/) - SQLAlchemy ORM
  ↓
Database (SQLite/PostgreSQL)
```

### 인증 시스템

- JWT 토큰을 httpOnly 쿠키에 저장
- `CurrentUser`: 인증 필수 의존성
- `CurrentUserOptional`: 인증 선택 의존성
- `app/api/deps.py`에서 의존성 정의

### HTMX 패턴

- 파셜 라우터가 HTML 조각 반환
- `HX-Trigger` 헤더로 토스트/모달 제어
- 템플릿: `templates/partials/` 하위 구조

## 새 기능 추가 순서

1. `app/models/` - SQLAlchemy 모델
2. `app/schemas/` - Pydantic 스키마
3. `app/services/` - 비즈니스 로직
4. `app/api/v1/` - REST API
5. `app/partials/` - HTMX 파셜
6. `templates/` - Jinja2 템플릿

## 주의사항

- 기본 포트는 **8001** (8000 아님)
- 비동기 DB: `aiosqlite` 사용
- 순환 import 방지: `TYPE_CHECKING` 블록 사용
- 테스트는 별도 DB(`test.db`) 사용
