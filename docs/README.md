# FastAPI + Jinja2 + HTMX 보일러플레이트 문서

이 문서는 FastAPI + Jinja2 + HTMX 보일러플레이트의 상세 가이드를 제공합니다.

## 문서 구조

### 1. 프로젝트 개요
- [프로젝트 소개](./01-project-overview.md) - 프로젝트 목적, 특징, 구조
- [빠른 시작 가이드](./02-quick-start.md) - 설치 및 실행 방법

### 2. 기술 스택 가이드
- [FastAPI 가이드](./03-fastapi-guide.md) - FastAPI 문법 및 사용법
- [Jinja2 가이드](./04-jinja2-guide.md) - Jinja2 템플릿 문법
- [HTMX 가이드](./05-htmx-guide.md) - HTMX 사용법 및 패턴
- [Alpine.js 가이드](./06-alpinejs-guide.md) - Alpine.js 기본 사용법
- [SQLAlchemy 가이드](./07-sqlalchemy-guide.md) - 데이터베이스 ORM

### 3. 프로젝트 구조
- [아키텍처 설명](./08-architecture.md) - 프로젝트 아키텍처
- [디렉토리 구조](./09-directory-structure.md) - 파일 및 폴더 구조

### 4. 개발 가이드
- [개발 환경 설정](./10-development-setup.md) - 개발 환경 구성
- [테스트 가이드](./11-testing-guide.md) - 테스트 작성 및 실행
- [배포 가이드](./12-deployment-guide.md) - 배포 방법

### 5. API 레퍼런스
- [API 엔드포인트](./13-api-reference.md) - API 문서

## 빠른 참조

### 로컬 실행
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env

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

## 기여하기

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다.

## 라이선스

MIT License
