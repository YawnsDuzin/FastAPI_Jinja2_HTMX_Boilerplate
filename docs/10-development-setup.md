# 개발 환경 설정

## 1. 필수 도구

### 1.1 Python 설치

Python 3.11 이상이 필요합니다.

```bash
# 버전 확인
python --version
# Python 3.11.x 이상

# pyenv 사용 시
pyenv install 3.12.0
pyenv local 3.12.0
```

### 1.2 가상환경 설정

```bash
# venv 사용
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# poetry 사용 (선택)
poetry install
poetry shell
```

## 2. 프로젝트 설정

### 2.1 의존성 설치

```bash
# 프로덕션 의존성
pip install -r requirements.txt

# 개발 의존성 포함
pip install -r requirements-dev.txt
```

### 2.2 환경 변수 설정

```bash
# 환경 파일 복사
cp .env.example .env

# .env 파일 편집
nano .env  # 또는 원하는 에디터
```

필수 환경 변수:

```env
APP_ENV=development
DEBUG=true
SECRET_KEY=your-development-secret-key
JWT_SECRET_KEY=your-jwt-development-secret
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

### 2.3 데이터베이스 초기화

```bash
# 마이그레이션 적용
alembic upgrade head

# 새 마이그레이션 생성 (모델 변경 시)
alembic revision --autogenerate -m "Description"
```

## 3. 개발 서버 실행

### 3.1 기본 실행

```bash
# 개발 모드 (자동 리로드)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 또는
python -m uvicorn app.main:app --reload
```

### 3.2 디버그 모드

```bash
# 상세 로깅
uvicorn app.main:app --reload --log-level debug
```

## 4. 코드 품질 도구

### 4.1 코드 포맷팅

```bash
# Black으로 포맷팅
black app tests

# isort로 import 정렬
isort app tests
```

### 4.2 린팅

```bash
# Ruff 린팅
ruff check app tests

# 자동 수정
ruff check --fix app tests
```

### 4.3 타입 검사

```bash
# mypy 타입 검사
mypy app
```

### 4.4 pre-commit 설정

```bash
# pre-commit 설치
pre-commit install

# 수동 실행
pre-commit run --all-files
```

`.pre-commit-config.yaml` 예시:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
```

## 5. 테스트

### 5.1 테스트 실행

```bash
# 전체 테스트
pytest

# 상세 출력
pytest -v

# 특정 파일
pytest tests/test_api/test_auth.py

# 특정 테스트
pytest tests/test_api/test_auth.py::test_login -v
```

### 5.2 커버리지

```bash
# 커버리지 측정
pytest --cov=app

# HTML 리포트
pytest --cov=app --cov-report=html
```

## 6. IDE 설정

### 6.1 VS Code

`.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

추천 확장:
- Python
- Pylance
- Black Formatter
- Ruff
- Python Test Explorer

### 6.2 PyCharm

1. **인터프리터 설정**: File → Settings → Project → Python Interpreter
2. **Black 설정**: File → Settings → Tools → Black
3. **테스트 설정**: Run → Edit Configurations → pytest

## 7. Docker 개발

### 7.1 Docker Compose 개발 모드

```bash
# 개발 모드 실행
docker-compose --profile dev up

# 재빌드
docker-compose --profile dev up --build
```

### 7.2 컨테이너 접속

```bash
# 앱 컨테이너 접속
docker-compose exec app-dev bash

# 로그 확인
docker-compose logs -f app-dev
```

## 8. 디버깅

### 8.1 VS Code 디버거

`.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true
    },
    {
      "name": "Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"]
    }
  ]
}
```

### 8.2 로깅

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("디버그 메시지")
logger.info("정보 메시지")
logger.warning("경고 메시지")
logger.error("에러 메시지")
```

### 8.3 SQL 로깅

```python
# database.py
engine = create_async_engine(
    settings.database_url,
    echo=True,  # SQL 로깅 활성화
)
```

## 9. 유용한 명령어

```bash
# 의존성 업데이트
pip install --upgrade -r requirements.txt

# 캐시 정리
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 데이터베이스 초기화
rm app.db && alembic upgrade head

# 포트 확인
lsof -i :8001
```

## 10. 문제 해결

### ImportError
```bash
# PYTHONPATH 설정
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### 포트 충돌
```bash
# 프로세스 종료
kill $(lsof -t -i:8001)
```

### 마이그레이션 오류
```bash
# 마이그레이션 히스토리 확인
alembic history

# 특정 버전으로 이동
alembic upgrade <revision>
alembic downgrade <revision>
```
