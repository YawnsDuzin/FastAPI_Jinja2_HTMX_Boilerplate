# 📖 용어 사전 (Glossary)

이 문서는 보일러플레이트에서 사용되는 기술 용어들을 초보자도 이해할 수 있도록 설명합니다.

---

## 목차

- [일반 웹 개발 용어](#일반-웹-개발-용어)
- [Python / FastAPI 용어](#python--fastapi-용어)
- [데이터베이스 / SQLAlchemy 용어](#데이터베이스--sqlalchemy-용어)
- [인증 / 보안 용어](#인증--보안-용어)
- [HTMX 용어](#htmx-용어)
- [Alpine.js 용어](#alpinejs-용어)
- [TailwindCSS 용어](#tailwindcss-용어)
- [개발 도구 용어](#개발-도구-용어)

---

## 일반 웹 개발 용어

### API (Application Programming Interface)
프로그램들이 서로 통신하기 위한 규약입니다. 웹 API는 HTTP를 통해 데이터를 주고받습니다.

```
클라이언트 → HTTP 요청 → 서버 → HTTP 응답 → 클라이언트
```

### REST (Representational State Transfer)
API 설계 방식 중 하나입니다. HTTP 메서드(GET, POST, PUT, DELETE)와 URL로 리소스를 조작합니다.

| 메서드 | 의미 | URL 예시 | 설명 |
|--------|------|----------|------|
| GET | 조회 | `/users` | 사용자 목록 조회 |
| GET | 조회 | `/users/1` | ID가 1인 사용자 조회 |
| POST | 생성 | `/users` | 새 사용자 생성 |
| PUT | 전체 수정 | `/users/1` | 사용자 전체 정보 수정 |
| PATCH | 부분 수정 | `/users/1` | 사용자 일부 정보 수정 |
| DELETE | 삭제 | `/users/1` | 사용자 삭제 |

### CRUD
데이터 처리의 4가지 기본 작업입니다.

- **C**reate (생성) - POST
- **R**ead (조회) - GET
- **U**pdate (수정) - PUT/PATCH
- **D**elete (삭제) - DELETE

### HTTP Status Code (상태 코드)
서버 응답의 결과를 나타내는 숫자 코드입니다.

| 코드 | 의미 | 설명 |
|------|------|------|
| 200 | OK | 요청 성공 |
| 201 | Created | 생성 성공 |
| 204 | No Content | 성공 (응답 본문 없음) |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 권한 없음 |
| 404 | Not Found | 리소스 없음 |
| 422 | Unprocessable Entity | 검증 실패 |
| 500 | Internal Server Error | 서버 오류 |

### JSON (JavaScript Object Notation)
데이터를 주고받을 때 사용하는 텍스트 형식입니다.

```json
{
  "name": "홍길동",
  "age": 30,
  "hobbies": ["독서", "영화"],
  "address": {
    "city": "서울",
    "zip": "12345"
  }
}
```

### SPA (Single Page Application)
페이지 전체를 새로고침하지 않고 필요한 부분만 업데이트하는 웹 애플리케이션입니다.

- **장점**: 빠른 사용자 경험
- **예시**: Gmail, Facebook
- **이 보일러플레이트**: HTMX로 SPA처럼 동작

### SSR (Server-Side Rendering)
서버에서 HTML을 완성하여 전송하는 방식입니다.

- **장점**: SEO 유리, 초기 로딩 빠름
- **이 보일러플레이트**: Jinja2로 SSR 구현

### AJAX (Asynchronous JavaScript and XML)
페이지 새로고침 없이 서버와 데이터를 주고받는 기술입니다.

```
사용자 클릭 → JavaScript 요청 → 서버 처리 → 부분 업데이트
```

### Cookie (쿠키)
브라우저에 저장되는 작은 데이터입니다. 서버가 설정하고 브라우저가 자동 전송합니다.

```
서버: Set-Cookie: session_id=abc123; HttpOnly; Secure
브라우저: Cookie: session_id=abc123 (매 요청 시 자동 전송)
```

### CORS (Cross-Origin Resource Sharing)
다른 도메인에서 API에 접근하는 것을 허용하는 메커니즘입니다.

```
프론트엔드 (localhost:3000) → API (localhost:8000)
                               ↓
                         CORS 설정 필요
```

---

## Python / FastAPI 용어

### ASGI (Asynchronous Server Gateway Interface)
비동기 Python 웹 서버 인터페이스입니다. FastAPI가 사용합니다.

```
웹 요청 → ASGI 서버 (uvicorn) → FastAPI 앱
```

### Uvicorn
ASGI 서버입니다. FastAPI 앱을 실행합니다.

```bash
uvicorn app.main:app --reload
#        ↑      ↑        ↑
#      모듈   변수명   자동 재시작
```

### Router (라우터)
URL 경로와 처리 함수를 연결합니다.

```python
router = APIRouter()

@router.get("/users")      # GET /users 요청을
async def list_users():    # 이 함수가 처리
    return {"users": []}
```

### Endpoint (엔드포인트)
API의 특정 URL 경로입니다. 하나의 기능을 담당합니다.

```
POST /api/v1/auth/login    → 로그인 엔드포인트
GET  /api/v1/users/me      → 내 정보 조회 엔드포인트
```

### Dependency Injection (의존성 주입)
함수가 필요로 하는 객체를 외부에서 제공받는 패턴입니다.

```python
# 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용
@app.get("/items")
async def get_items(db: Session = Depends(get_db)):
    # db가 자동으로 주입됨
    return db.query(Item).all()
```

### Middleware (미들웨어)
요청/응답을 중간에서 처리하는 레이어입니다.

```
요청 → 미들웨어1 → 미들웨어2 → 라우터 → 미들웨어2 → 미들웨어1 → 응답
```

예시: 로깅, CORS 처리, 인증 확인

### Lifespan (수명주기)
앱 시작/종료 시 실행할 코드를 정의합니다.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시
    await init_db()
    yield
    # 종료 시
    await close_db()
```

### Pydantic
데이터 검증 및 직렬화 라이브러리입니다.

```python
class User(BaseModel):
    name: str                    # 필수 문자열
    age: int = 0                 # 기본값 있는 정수
    email: Optional[str] = None  # 선택적 문자열

# 자동 검증
user = User(name="홍길동", age="30")  # age가 int로 변환됨
user = User(name=123)  # ValidationError 발생
```

### Schema (스키마)
데이터의 구조를 정의합니다. Pydantic 모델로 작성합니다.

| 스키마 유형 | 용도 | 예시 |
|------------|------|------|
| Create | 생성 요청 | `UserCreate` |
| Update | 수정 요청 | `UserUpdate` |
| Response | API 응답 | `User` |

### async/await (비동기)
동시에 여러 작업을 처리할 수 있게 합니다.

```python
# 동기 (블로킹)
def get_user():
    result = db.query(User).first()  # 완료될 때까지 대기
    return result

# 비동기 (논블로킹)
async def get_user():
    result = await db.execute(query)  # 대기 중 다른 요청 처리 가능
    return result
```

---

## 데이터베이스 / SQLAlchemy 용어

### ORM (Object-Relational Mapping)
데이터베이스 테이블을 Python 클래스로 다루는 기술입니다.

```python
# SQL 없이 Python 코드로 DB 조작
user = User(name="홍길동", email="hong@example.com")
db.add(user)
await db.commit()

# 실제 실행되는 SQL:
# INSERT INTO users (name, email) VALUES ('홍길동', 'hong@example.com')
```

### Model (모델)
데이터베이스 테이블을 정의하는 Python 클래스입니다.

```python
class User(Base):
    __tablename__ = "users"        # 테이블 이름

    id = Column(Integer, primary_key=True)   # 컬럼 정의
    name = Column(String(100), nullable=False)
```

### Session (세션)
데이터베이스 연결 및 트랜잭션을 관리하는 객체입니다.

```python
async with get_session() as session:
    # 여러 작업을 하나의 트랜잭션으로
    user = await session.get(User, 1)
    user.name = "새이름"
    await session.commit()  # 모든 변경 저장
```

### Query (쿼리)
데이터베이스에 보내는 요청입니다.

```python
# SQLAlchemy 2.0 스타일
query = select(User).where(User.age > 18).order_by(User.name)
result = await session.execute(query)
users = result.scalars().all()
```

### Migration (마이그레이션)
데이터베이스 스키마 변경을 버전 관리합니다.

```bash
# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Add email column"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### Relationship (관계)
테이블 간의 연결을 정의합니다.

```python
class User(Base):
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")  # 1:N 관계

class Post(Base):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))    # 외래키
    author = relationship("User", back_populates="posts")  # 역방향 관계
```

### Foreign Key (외래키)
다른 테이블의 기본키를 참조하는 컬럼입니다.

```python
# posts.author_id → users.id를 참조
author_id = Column(Integer, ForeignKey("users.id"))
```

---

## 인증 / 보안 용어

### JWT (JSON Web Token)
인증 정보를 담은 토큰입니다. 3개 파트로 구성됩니다.

```
xxxxx.yyyyy.zzzzz
  ↑      ↑      ↑
Header Payload Signature
```

```python
# 페이로드 예시
{
  "sub": "123",        # 사용자 ID
  "exp": 1700000000,   # 만료 시간
  "type": "access"     # 토큰 타입
}
```

### Access Token (액세스 토큰)
API 접근에 사용하는 짧은 수명의 토큰입니다.

- **수명**: 15분 ~ 1시간
- **용도**: 매 API 요청 시 전송
- **저장**: httpOnly 쿠키

### Refresh Token (리프레시 토큰)
새 Access Token을 발급받는 데 사용하는 긴 수명의 토큰입니다.

- **수명**: 7일 ~ 30일
- **용도**: Access Token 만료 시 갱신
- **저장**: httpOnly 쿠키

### httpOnly Cookie
JavaScript에서 접근할 수 없는 쿠키입니다.

```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,  # JavaScript 접근 불가 → XSS 방지
    secure=True,    # HTTPS에서만 전송
    samesite="lax"  # CSRF 방지
)
```

### Hash (해시)
원본 데이터를 고정 길이의 문자열로 변환합니다. 역변환 불가능합니다.

```python
# 비밀번호 해싱 (bcrypt)
password = "mypassword123"
hashed = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.n"

# 검증 시
verify_password("mypassword123", hashed)  # True
```

### Salt (솔트)
해시에 추가하는 랜덤 데이터입니다. 같은 비밀번호도 다른 해시값을 가집니다.

```
비밀번호: "password123"
Salt 1: "abc" → 해시: "xyz..."
Salt 2: "def" → 해시: "uvw..."  (다른 결과)
```

### XSS (Cross-Site Scripting)
악성 스크립트를 주입하는 공격입니다.

```html
<!-- 위험: 사용자 입력을 그대로 출력 -->
<div>{{ user_input }}</div>

<!-- 입력값: <script>alert('해킹!')</script> -->
```

**방어**: Jinja2 자동 이스케이프, httpOnly 쿠키

### CSRF (Cross-Site Request Forgery)
사용자 모르게 요청을 보내는 공격입니다.

**방어**: SameSite 쿠키, CSRF 토큰

---

## HTMX 용어

### hx-get, hx-post, hx-put, hx-delete
HTTP 요청을 보내는 속성입니다.

```html
<button hx-get="/api/items">조회</button>
<button hx-post="/api/items">생성</button>
<button hx-put="/api/items/1">수정</button>
<button hx-delete="/api/items/1">삭제</button>
```

### hx-target
응답을 넣을 요소를 지정합니다.

```html
<!-- 응답을 #result 요소에 넣음 -->
<button hx-get="/api/data" hx-target="#result">로드</button>
<div id="result"></div>
```

### hx-swap
응답을 어떻게 넣을지 지정합니다.

| 값 | 동작 |
|----|------|
| `innerHTML` | 내부 HTML 교체 (기본) |
| `outerHTML` | 요소 전체 교체 |
| `beforeend` | 끝에 추가 |
| `afterbegin` | 시작에 추가 |
| `delete` | 요소 삭제 |
| `none` | DOM 수정 안 함 |

```html
<!-- 목록 끝에 새 아이템 추가 -->
<div id="list">
    <div>아이템 1</div>
</div>
<button hx-post="/items" hx-target="#list" hx-swap="beforeend">
    추가
</button>
```

### hx-trigger
요청을 보낼 시점을 지정합니다.

```html
<!-- 클릭 시 (기본) -->
<button hx-get="/data" hx-trigger="click">클릭</button>

<!-- 입력 변경 후 500ms 대기 -->
<input hx-get="/search" hx-trigger="keyup changed delay:500ms">

<!-- 페이지 로드 시 -->
<div hx-get="/data" hx-trigger="load">로딩중...</div>

<!-- 화면에 보일 때 -->
<div hx-get="/more" hx-trigger="revealed">더보기</div>
```

### hx-indicator
요청 중 표시할 로딩 인디케이터입니다.

```html
<button hx-get="/data" hx-indicator="#spinner">로드</button>
<span id="spinner" class="htmx-indicator">로딩중...</span>
```

CSS:
```css
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline; }
```

### hx-boost
일반 링크를 AJAX로 변환합니다.

```html
<body hx-boost="true">
    <!-- 이 안의 모든 <a> 링크가 AJAX로 동작 -->
    <a href="/about">소개</a>
</body>
```

### Partial (파셜)
전체 페이지가 아닌 부분 HTML입니다.

```html
<!-- 전체 페이지 (base.html 상속) -->
{% extends "base.html" %}
{% block content %}...{% endblock %}

<!-- 파셜 (base.html 없이 부분만) -->
<div class="item">{{ item.name }}</div>
```

### HX-Trigger (응답 헤더)
서버에서 클라이언트 이벤트를 트리거합니다.

```python
# Python (FastAPI)
return HTMLResponse(
    content="<div>완료</div>",
    headers={
        "HX-Trigger": '{"showToast": {"message": "저장됨!"}}'
    }
)
```

```html
<!-- 클라이언트에서 이벤트 수신 -->
<div @showToast.window="alert($event.detail.message)"></div>
```

---

## Alpine.js 용어

### x-data
컴포넌트 상태를 정의합니다.

```html
<div x-data="{ count: 0, name: '홍길동' }">
    <!-- 이 안에서 count, name 사용 가능 -->
</div>
```

### x-show
조건에 따라 표시/숨김합니다 (display: none).

```html
<div x-data="{ open: false }">
    <button @click="open = !open">토글</button>
    <div x-show="open">열림!</div>
</div>
```

### x-if
조건에 따라 DOM에서 추가/제거합니다.

```html
<template x-if="isLoggedIn">
    <span>환영합니다!</span>
</template>
```

### x-for
반복 렌더링합니다.

```html
<div x-data="{ items: ['사과', '바나나', '포도'] }">
    <template x-for="item in items">
        <div x-text="item"></div>
    </template>
</div>
```

### x-text, x-html
텍스트 또는 HTML을 바인딩합니다.

```html
<span x-text="name"></span>      <!-- 텍스트 (안전) -->
<span x-html="htmlContent"></span>  <!-- HTML (XSS 주의) -->
```

### x-bind (:)
속성을 동적으로 바인딩합니다.

```html
<img :src="imageUrl">
<button :disabled="isLoading">
<div :class="{ 'bg-red': hasError }">
```

### x-on (@)
이벤트 핸들러를 연결합니다.

```html
<button @click="count++">+1</button>
<input @keyup.enter="submit()">
<form @submit.prevent="handleSubmit()">
```

### x-model
양방향 바인딩입니다.

```html
<div x-data="{ email: '' }">
    <input x-model="email" type="email">
    <p>입력: <span x-text="email"></span></p>
</div>
```

### x-transition
표시/숨김 시 애니메이션입니다.

```html
<div x-show="open"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0"
     x-transition:enter-end="opacity-100">
</div>
```

---

## TailwindCSS 용어

### Utility Class (유틸리티 클래스)
하나의 CSS 속성을 적용하는 클래스입니다.

```html
<div class="bg-blue-500 text-white p-4 rounded-lg">
    <!--      배경색     글자색   패딩   모서리 -->
</div>
```

### Responsive Prefix (반응형 접두사)
화면 크기별로 다른 스타일을 적용합니다.

```html
<div class="w-full md:w-1/2 lg:w-1/3">
    <!-- 모바일: 100%, 태블릿: 50%, 데스크탑: 33% -->
</div>
```

| 접두사 | 최소 너비 |
|--------|-----------|
| (없음) | 0px |
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |
| `2xl:` | 1536px |

### Dark Mode (다크 모드)
`dark:` 접두사로 다크 모드 스타일을 적용합니다.

```html
<div class="bg-white dark:bg-gray-900 text-black dark:text-white">
    <!-- 라이트: 흰 배경, 검은 글자 -->
    <!-- 다크: 어두운 배경, 흰 글자 -->
</div>
```

### State Variants (상태 변형)
요소 상태에 따라 스타일을 적용합니다.

```html
<button class="bg-blue-500 hover:bg-blue-600 focus:ring-2 active:bg-blue-700">
    <!--         기본      마우스오버     포커스     클릭중 -->
</button>
```

---

## 개발 도구 용어

### Git
버전 관리 시스템입니다. 코드 변경 이력을 관리합니다.

```bash
git add .                    # 변경 파일 스테이징
git commit -m "메시지"       # 커밋 생성
git push origin main         # 원격에 업로드
git pull origin main         # 원격에서 다운로드
```

### Virtual Environment (가상 환경)
프로젝트별로 독립된 Python 패키지를 관리합니다.

```bash
python -m venv venv    # 가상환경 생성
source venv/bin/activate  # 활성화 (Linux/Mac)
pip install -r requirements.txt  # 패키지 설치
```

### Docker
애플리케이션을 컨테이너로 패키징합니다.

```bash
docker build -t myapp .              # 이미지 빌드
docker run -p 8000:8000 myapp        # 컨테이너 실행
docker-compose up -d                 # 여러 서비스 실행
```

### Environment Variable (환경 변수)
설정 값을 코드 외부에서 관리합니다.

```bash
# .env 파일
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=mysecretkey123

# Python에서 사용
import os
db_url = os.getenv("DATABASE_URL")
```

### Hot Reload (핫 리로드)
코드 변경 시 자동으로 서버를 재시작합니다.

```bash
uvicorn app.main:app --reload
#                       ↑
#                   핫 리로드 활성화
```

---

## 더 알아보기

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [HTMX 공식 문서](https://htmx.org/docs/)
- [Alpine.js 공식 문서](https://alpinejs.dev/)
- [TailwindCSS 공식 문서](https://tailwindcss.com/docs)
