# 빠른 시작 가이드

이 가이드는 Windows, macOS, Linux(Ubuntu), 라즈베리파이에서 프로젝트를 설치하고 실행하는 방법을 설명합니다.

## 1. 요구 사항

### 1.1 시스템 요구사항

| 항목 | 최소 사양 | 권장 사양 |
|------|----------|----------|
| Python | 3.11 이상 | 3.12 |
| RAM | 1GB | 2GB 이상 |
| 디스크 | 500MB | 1GB 이상 |
| OS | Windows 10+, macOS 10.15+, Ubuntu 20.04+, Raspberry Pi OS |

### 1.2 필수 소프트웨어

- **Python 3.11+**: 프로그래밍 언어
- **pip**: Python 패키지 관리자
- **Git**: 버전 관리
- **(선택) Docker**: 컨테이너 실행 환경

---

## 2. Python 설치

### Windows

#### 방법 1: 공식 설치 프로그램 (권장)

1. [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.12 다운로드
2. 설치 프로그램 실행
3. **⚠️ 중요**: "Add Python to PATH" 체크박스 반드시 선택
4. "Install Now" 클릭

```powershell
# 설치 확인 (PowerShell 또는 명령 프롬프트)
python --version
# Python 3.12.x

pip --version
# pip 24.x.x
```

#### 방법 2: winget 사용

```powershell
# Windows Package Manager로 설치
winget install Python.Python.3.12

# 터미널 재시작 후 확인
python --version
```

#### 방법 3: Microsoft Store

1. Microsoft Store 앱 열기
2. "Python 3.12" 검색
3. 설치 클릭

### macOS

#### 방법 1: 공식 설치 프로그램

1. [Python 공식 사이트](https://www.python.org/downloads/)에서 macOS용 다운로드
2. .pkg 파일 실행하여 설치

#### 방법 2: Homebrew (권장)

```bash
# Homebrew 설치 (없는 경우)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python@3.12

# 확인
python3 --version
# Python 3.12.x
```

#### 방법 3: pyenv (여러 버전 관리 시)

```bash
# pyenv 설치
brew install pyenv

# 쉘 설정 추가 (~/.zshrc 또는 ~/.bash_profile)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 터미널 재시작 또는
source ~/.zshrc

# Python 설치
pyenv install 3.12.0
pyenv global 3.12.0

# 확인
python --version
```

### Linux (Ubuntu/Debian)

```bash
# 패키지 목록 업데이트
sudo apt update

# 필수 패키지 설치
sudo apt install -y software-properties-common

# Python PPA 추가 (최신 버전용)
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

# Python 3.12 설치
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# python3 명령을 python3.12로 설정 (선택)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# 확인
python3 --version
# Python 3.12.x
```

### 라즈베리파이 (Raspberry Pi OS)

라즈베리파이는 기본적으로 Python이 설치되어 있지만, 최신 버전이 필요합니다.

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 빌드 도구 설치
sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev

# pyenv 설치 (권장 - 최신 Python 설치 가능)
curl https://pyenv.run | bash

# 쉘 설정 추가 (~/.bashrc)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 적용
source ~/.bashrc

# Python 설치 (라즈베리파이에서는 시간이 걸림)
pyenv install 3.12.0
pyenv global 3.12.0

# 확인
python --version
```

> **💡 라즈베리파이 팁**: 라즈베리파이 4 (4GB 이상)에서 원활하게 동작합니다. 라즈베리파이 3나 Zero는 메모리 제한으로 빌드 시간이 오래 걸릴 수 있습니다.

---

## 3. 저장소 클론

### Git 설치

**Windows:**
```powershell
# Git 설치 (winget)
winget install Git.Git

# 또는 https://git-scm.com/download/win 에서 다운로드
```

**macOS:**
```bash
# Xcode Command Line Tools와 함께 설치됨
xcode-select --install

# 또는 Homebrew로
brew install git
```

**Linux/라즈베리파이:**
```bash
sudo apt install -y git
```

### 저장소 클론

```bash
# 프로젝트 클론
git clone https://github.com/YawnsDuzin/FastAPI_Jinja2_HTMX_Boilerplate.git

# 프로젝트 폴더로 이동
cd FastAPI_Jinja2_HTMX_Boilerplate
```

---

## 4. 가상환경 설정

가상환경은 프로젝트별로 독립된 Python 환경을 만들어 패키지 충돌을 방지합니다.

### Windows (PowerShell)

```powershell
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 활성화 확인 (프롬프트에 (venv) 표시)
# (venv) PS C:\path\to\project>
```

> **⚠️ PowerShell 실행 정책 오류 시:**
> ```powershell
> # 현재 사용자에 대해 스크립트 실행 허용
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Windows (명령 프롬프트 CMD)

```cmd
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate.bat

# 활성화 확인 (프롬프트에 (venv) 표시)
# (venv) C:\path\to\project>
```

### Windows (Git Bash)

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/Scripts/activate

# 활성화 확인
# (venv) user@hostname MINGW64 /c/path/to/project
```

### macOS / Linux / 라즈베리파이

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 활성화 확인 (프롬프트에 (venv) 표시)
# (venv) user@hostname:~/project$
```

### 가상환경 비활성화 (모든 OS 공통)

```bash
deactivate
```

---

## 5. 의존성 설치

가상환경이 활성화된 상태에서 실행하세요.

### 기본 설치

```bash
# 프로덕션 의존성만 설치
pip install -r requirements.txt
```

### 개발 환경 (권장)

```bash
# 개발 도구 포함 설치
pip install -r requirements-dev.txt
```

### 설치 확인

```bash
# 설치된 패키지 목록
pip list

# FastAPI 확인
pip show fastapi
```

### 문제 해결

**Windows에서 설치 오류 시:**
```powershell
# pip 업그레이드
python -m pip install --upgrade pip

# 캐시 없이 설치
pip install --no-cache-dir -r requirements.txt
```

**Linux/macOS에서 권한 오류 시:**
```bash
# 가상환경 활성화 확인
which python
# /path/to/project/venv/bin/python 이어야 함

# 가상환경 없이 설치하려면 (권장하지 않음)
pip install --user -r requirements.txt
```

**라즈베리파이에서 빌드 오류 시:**
```bash
# 필요한 빌드 도구 설치
sudo apt install -y python3-dev libffi-dev libssl-dev

# 다시 설치
pip install -r requirements.txt
```

---

## 6. 환경 변수 설정

### 환경 파일 생성

**Windows (PowerShell):**
```powershell
# 예시 파일 복사
Copy-Item .env.example .env
```

**Windows (CMD):**
```cmd
copy .env.example .env
```

**macOS / Linux / 라즈베리파이:**
```bash
cp .env.example .env
```

### 환경 파일 편집

`.env` 파일을 편집기로 열어 수정합니다.

**Windows:**
```powershell
# 메모장으로 열기
notepad .env

# 또는 VS Code로 열기
code .env
```

**macOS:**
```bash
# 기본 편집기
open -e .env

# 또는 nano
nano .env

# 또는 VS Code
code .env
```

**Linux / 라즈베리파이:**
```bash
# nano 편집기
nano .env

# 또는 vim
vim .env
```

### 주요 환경 변수 설명

```env
# 애플리케이션 설정
APP_NAME=FastAPI-HTMX-Boilerplate    # 앱 이름
APP_ENV=development                   # 환경 (development, production)
DEBUG=true                            # 디버그 모드 (production에서는 false)

# 보안 키 (반드시 변경!)
SECRET_KEY=your-secret-key-change-me          # 앱 비밀키
JWT_SECRET_KEY=your-jwt-secret-change-me      # JWT 서명 키

# 데이터베이스
DATABASE_URL=sqlite+aiosqlite:///./app.db     # SQLite (개발용)
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname  # PostgreSQL

# JWT 설정
ACCESS_TOKEN_EXPIRE_MINUTES=30        # 액세스 토큰 만료 시간 (분)
REFRESH_TOKEN_EXPIRE_DAYS=7           # 리프레시 토큰 만료 시간 (일)
```

### 비밀키 생성 방법

```bash
# Python으로 랜덤 키 생성
python -c "import secrets; print(secrets.token_urlsafe(32))"
# 예: Ks8j2L_xN7pQ3mR5vY9wB1cD4eF6gH8i
```

생성된 키를 `.env` 파일의 `SECRET_KEY`와 `JWT_SECRET_KEY`에 각각 다른 값으로 설정하세요.

---

## 7. 데이터베이스 설정

### SQLite (기본값, 개발용)

SQLite는 별도 설치 없이 바로 사용 가능합니다.

```bash
# 마이그레이션 실행 (데이터베이스 테이블 생성)
alembic upgrade head

# 확인 - app.db 파일이 생성됨
```

**Windows:**
```powershell
dir app.db
```

**macOS/Linux:**
```bash
ls -la app.db
```

### PostgreSQL (프로덕션 권장)

#### PostgreSQL 설치

**Windows:**
```powershell
# winget으로 설치
winget install PostgreSQL.PostgreSQL

# 또는 https://www.postgresql.org/download/windows/ 에서 다운로드
```

**macOS:**
```bash
# Homebrew로 설치
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu):**
```bash
# 설치
sudo apt install -y postgresql postgresql-contrib

# 서비스 시작
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**라즈베리파이:**
```bash
# 설치
sudo apt install -y postgresql postgresql-contrib

# 서비스 시작
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 데이터베이스 생성

```bash
# PostgreSQL 접속
sudo -u postgres psql

# 데이터베이스 및 사용자 생성
CREATE DATABASE fastapi_htmx;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE fastapi_htmx TO myuser;
\q
```

#### 환경 변수 수정

`.env` 파일:
```env
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost:5432/fastapi_htmx
```

#### 마이그레이션 실행

```bash
alembic upgrade head
```

---

## 8. 개발 서버 실행

### 기본 실행

```bash
# 개발 서버 실행 (자동 리로드)
python run.py

# 또는 uvicorn 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### OS별 실행 확인

**Windows:**
```powershell
# PowerShell에서 실행
python run.py

# 브라우저에서 확인
start http://localhost:8001
```

**macOS:**
```bash
# 실행
python run.py

# 브라우저에서 확인
open http://localhost:8001
```

**Linux / 라즈베리파이:**
```bash
# 실행
python run.py

# 다른 터미널에서 확인
curl http://localhost:8001
```

### 서버 접속 정보

| URL | 설명 |
|-----|------|
| http://localhost:8001 | 메인 애플리케이션 |
| http://localhost:8001/docs | Swagger API 문서 |
| http://localhost:8001/redoc | ReDoc API 문서 |

### 외부 접속 허용 (라즈베리파이 등)

다른 기기에서 접속하려면 `--host 0.0.0.0` 옵션을 사용합니다.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

그러면 `http://<라즈베리파이-IP>:8001`로 접속 가능합니다.

라즈베리파이 IP 확인:
```bash
hostname -I
# 예: 192.168.1.100
```

---

## 9. Docker 실행 (선택)

### Docker 설치

**Windows:**
- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) 설치

**macOS:**
- [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) 설치

**Linux (Ubuntu):**
```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 재로그인 또는
newgrp docker
```

**라즈베리파이:**
```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 재로그인 필요
```

### Docker Compose 실행

```bash
# 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

### 개발 모드

```bash
# 개발 모드로 실행 (핫 리로드)
docker-compose --profile dev up
```

### PostgreSQL과 함께 실행

```bash
# PostgreSQL 프로필 포함
docker-compose --profile postgres up -d
```

---

## 10. 첫 사용자 생성

### 웹 인터페이스로 가입

1. 브라우저에서 http://localhost:8001/register 접속
2. 이메일, 사용자명, 비밀번호 입력
3. 회원가입 완료 후 자동 로그인

### API로 가입 (curl)

**Windows (PowerShell):**
```powershell
# 회원가입
Invoke-RestMethod -Uri "http://localhost:8001/api/v1/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"email": "user@example.com", "username": "testuser", "password": "password123"}'
```

**macOS / Linux / 라즈베리파이:**
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

---

## 11. 프로젝트 탐색

### 주요 페이지

| URL | 설명 | 인증 필요 |
|-----|------|----------|
| `/` | 홈페이지 | ❌ |
| `/about` | 소개 페이지 | ❌ |
| `/login` | 로그인 | ❌ |
| `/register` | 회원가입 | ❌ |
| `/dashboard` | 대시보드 | ✅ |
| `/items` | 아이템 관리 | ✅ |
| `/profile` | 프로필 설정 | ✅ |

### API 엔드포인트

| 메서드 | URL | 설명 |
|--------|-----|------|
| `POST` | `/api/v1/auth/register` | 회원가입 |
| `POST` | `/api/v1/auth/login` | 로그인 |
| `POST` | `/api/v1/auth/logout` | 로그아웃 |
| `GET` | `/api/v1/auth/me` | 현재 사용자 정보 |
| `GET` | `/api/v1/items` | 아이템 목록 |
| `POST` | `/api/v1/items` | 아이템 생성 |
| `GET` | `/api/v1/items/{id}` | 아이템 조회 |
| `PATCH` | `/api/v1/items/{id}` | 아이템 수정 |
| `DELETE` | `/api/v1/items/{id}` | 아이템 삭제 |

---

## 12. 테스트 실행

```bash
# 전체 테스트
pytest

# 상세 출력
pytest -v

# 커버리지 포함
pytest --cov=app

# 특정 테스트 파일
pytest tests/test_api/test_auth.py -v
```

---

## 13. 코드 품질 도구

```bash
# 코드 포맷팅
black app tests
isort app tests

# 린트 검사
ruff check app tests

# 타입 검사
mypy app
```

---

## 14. 문제 해결

### Python을 찾을 수 없음

**Windows:**
```powershell
# PATH에 Python 추가 확인
$env:Path -split ';' | Select-String -Pattern "Python"

# 없으면 Python 재설치 시 "Add Python to PATH" 체크
```

**macOS/Linux:**
```bash
# python3 사용
python3 --version

# 또는 alias 설정
alias python=python3
```

### 포트 충돌 (8001 포트 사용 중)

**Windows:**
```powershell
# 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8001

# 프로세스 종료 (PID로)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# 포트 사용 중인 프로세스 확인
lsof -i :8001

# 프로세스 종료
kill -9 $(lsof -t -i:8001)

# 또는 다른 포트로 실행
uvicorn app.main:app --reload --port 8002
```

### 데이터베이스 초기화

```bash
# SQLite 데이터베이스 삭제 후 재생성
rm app.db          # Linux/macOS
del app.db         # Windows

# 마이그레이션 재실행
alembic upgrade head
```

### 의존성 설치 오류

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 캐시 정리 후 재설치
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### 가상환경 활성화 실패 (Windows PowerShell)

```powershell
# 실행 정책 변경
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 다시 활성화
.\venv\Scripts\Activate.ps1
```

### 라즈베리파이 메모리 부족

```bash
# 스왑 메모리 증가
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=2048 으로 변경
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

---

## 15. 다음 단계

1. 📁 [디렉토리 구조](./09-directory-structure.md) 이해하기
2. 🚀 [FastAPI 가이드](./03-fastapi-guide.md) 읽기
3. 🔄 [HTMX 가이드](./05-htmx-guide.md)로 동적 UI 구현
4. 🎨 [Jinja2 가이드](./04-jinja2-guide.md)로 템플릿 작성
5. 🗄️ [SQLAlchemy 가이드](./07-sqlalchemy-guide.md)로 DB 작업
