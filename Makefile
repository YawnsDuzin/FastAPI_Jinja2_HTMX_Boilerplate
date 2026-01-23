# =============================================================================
# FastAPI + Jinja2 + HTMX Boilerplate - Makefile
# =============================================================================
#
# 자주 사용하는 명령어를 단축하여 실행할 수 있습니다.
#
# 사용법:
#     make <명령어>
#
# 예시:
#     make run      - 개발 서버 실행
#     make test     - 테스트 실행
#     make migrate  - DB 마이그레이션 적용
#
# 명령어 목록 보기:
#     make help
#
# =============================================================================

# 기본 설정
.PHONY: help install run dev test lint format clean docker docker-down migrate shell

# 기본 명령어 (make만 입력 시)
.DEFAULT_GOAL := help

# =============================================================================
# 도움말
# =============================================================================

help:  ## 사용 가능한 명령어 목록 표시
	@echo ""
	@echo "📋 사용 가능한 명령어:"
	@echo ""
	@echo "  🚀 실행"
	@echo "    make run          개발 서버 실행 (자동 재시작)"
	@echo "    make run-prod     프로덕션 서버 실행"
	@echo ""
	@echo "  📦 설치"
	@echo "    make install      의존성 설치"
	@echo "    make install-dev  개발 의존성 포함 설치"
	@echo "    make venv         가상환경 생성"
	@echo ""
	@echo "  🧪 테스트 & 품질"
	@echo "    make test         테스트 실행"
	@echo "    make test-cov     테스트 + 커버리지 리포트"
	@echo "    make lint         린트 검사 (ruff)"
	@echo "    make format       코드 포맷팅 (ruff)"
	@echo "    make check        린트 + 타입 검사"
	@echo ""
	@echo "  🗄️  데이터베이스"
	@echo "    make migrate      마이그레이션 적용"
	@echo "    make migration    새 마이그레이션 생성 (MSG 필요)"
	@echo "    make db-reset     DB 초기화 (주의!)"
	@echo ""
	@echo "  🐳 Docker"
	@echo "    make docker       Docker Compose 실행"
	@echo "    make docker-down  Docker Compose 중지"
	@echo "    make docker-build Docker 이미지 빌드"
	@echo "    make docker-logs  Docker 로그 보기"
	@echo ""
	@echo "  🧹 기타"
	@echo "    make clean        캐시 및 임시 파일 삭제"
	@echo "    make shell        Python 셸 실행"
	@echo ""

# =============================================================================
# 실행 (Run)
# =============================================================================

run:  ## 개발 서버 실행 (자동 재시작)
	@echo "🚀 개발 서버 시작..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-prod:  ## 프로덕션 서버 실행
	@echo "🚀 프로덕션 서버 시작..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

dev: run  ## run의 별칭

# =============================================================================
# 설치 (Install)
# =============================================================================

venv:  ## 가상환경 생성
	@echo "📦 가상환경 생성 중..."
	python3 -m venv venv
	@echo "✅ 가상환경 생성 완료"
	@echo ""
	@echo "활성화 방법:"
	@echo "  Linux/Mac: source venv/bin/activate"
	@echo "  Windows:   venv\\Scripts\\activate"

install:  ## 프로덕션 의존성 설치
	@echo "📦 의존성 설치 중..."
	pip install -r requirements.txt
	@echo "✅ 설치 완료"

install-dev:  ## 개발 의존성 포함 설치
	@echo "📦 개발 의존성 설치 중..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "✅ 설치 완료"

# =============================================================================
# 테스트 & 품질 (Test & Quality)
# =============================================================================

test:  ## 테스트 실행
	@echo "🧪 테스트 실행 중..."
	pytest tests/ -v

test-cov:  ## 테스트 + 커버리지 리포트
	@echo "🧪 테스트 + 커버리지 실행 중..."
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term
	@echo ""
	@echo "📊 HTML 리포트: htmlcov/index.html"

test-fast:  ## 빠른 테스트 (마지막 실패한 테스트만)
	pytest tests/ -v --lf

lint:  ## 린트 검사 (ruff)
	@echo "🔍 린트 검사 중..."
	ruff check app/ tests/
	@echo "✅ 린트 검사 완료"

format:  ## 코드 포맷팅 (ruff)
	@echo "🎨 코드 포맷팅 중..."
	ruff format app/ tests/
	ruff check app/ tests/ --fix
	@echo "✅ 포맷팅 완료"

type-check:  ## 타입 검사 (mypy)
	@echo "🔍 타입 검사 중..."
	mypy app/ --ignore-missing-imports

check: lint type-check  ## 린트 + 타입 검사

# =============================================================================
# 데이터베이스 (Database)
# =============================================================================

migrate:  ## 마이그레이션 적용 (최신 버전으로)
	@echo "🗄️ 마이그레이션 적용 중..."
	alembic upgrade head
	@echo "✅ 마이그레이션 완료"

migration:  ## 새 마이그레이션 생성 (사용: make migration MSG="메시지")
ifndef MSG
	$(error ❌ MSG가 필요합니다. 예: make migration MSG="Add users table")
endif
	@echo "🗄️ 마이그레이션 생성 중: $(MSG)"
	alembic revision --autogenerate -m "$(MSG)"
	@echo "✅ 마이그레이션 파일 생성됨"

migrate-down:  ## 마이그레이션 1단계 롤백
	@echo "🗄️ 마이그레이션 롤백 중..."
	alembic downgrade -1
	@echo "✅ 롤백 완료"

db-reset:  ## DB 초기화 (모든 데이터 삭제!)
	@echo "⚠️  경고: 모든 데이터가 삭제됩니다!"
	@read -p "계속하시겠습니까? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "🗄️ DB 초기화 중..."; \
		alembic downgrade base; \
		alembic upgrade head; \
		echo "✅ DB 초기화 완료"; \
	else \
		echo "❌ 취소됨"; \
	fi

# =============================================================================
# Docker
# =============================================================================

docker:  ## Docker Compose로 실행 (개발 모드)
	@echo "🐳 Docker Compose 시작..."
	docker-compose --profile dev up -d
	@echo "✅ 서비스 시작됨"
	@echo ""
	@echo "🌐 앱: http://localhost:8000"
	@echo "🗄️ DB: localhost:5432"

docker-down:  ## Docker Compose 중지
	@echo "🐳 Docker Compose 중지..."
	docker-compose down
	@echo "✅ 서비스 중지됨"

docker-build:  ## Docker 이미지 빌드
	@echo "🐳 Docker 이미지 빌드 중..."
	docker-compose build
	@echo "✅ 빌드 완료"

docker-logs:  ## Docker 로그 보기
	docker-compose logs -f

docker-shell:  ## Docker 컨테이너 셸 접속
	docker-compose exec app /bin/bash

docker-clean:  ## Docker 정리 (컨테이너, 볼륨)
	@echo "🧹 Docker 정리 중..."
	docker-compose down -v --remove-orphans
	@echo "✅ 정리 완료"

# =============================================================================
# 기타 (Misc)
# =============================================================================

clean:  ## 캐시 및 임시 파일 삭제
	@echo "🧹 캐시 정리 중..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ 정리 완료"

shell:  ## Python 셸 실행 (앱 컨텍스트)
	@echo "🐍 Python 셸 시작..."
	python -c "from app.main import app; print('앱 로드됨: app'); import code; code.interact(local=locals())"

tree:  ## 프로젝트 구조 출력
	@echo "📁 프로젝트 구조:"
	@tree -I 'venv|__pycache__|.git|htmlcov|.pytest_cache|.ruff_cache' -L 3

# =============================================================================
# 자주 사용하는 조합
# =============================================================================

setup: venv install-dev migrate  ## 프로젝트 초기 설정 (가상환경 + 설치 + 마이그레이션)
	@echo ""
	@echo "🎉 프로젝트 설정 완료!"
	@echo ""
	@echo "다음 단계:"
	@echo "  1. source venv/bin/activate"
	@echo "  2. cp .env.example .env"
	@echo "  3. make run"

ci: lint test  ## CI 파이프라인 (린트 + 테스트)

# =============================================================================
# 도움말 생성용 (내부)
# =============================================================================

# 이 부분은 help 명령어의 자동 생성을 위한 것입니다.
# ## 뒤에 오는 텍스트가 help에 표시됩니다.
