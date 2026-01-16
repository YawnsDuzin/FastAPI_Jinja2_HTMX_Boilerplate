# API 레퍼런스

## 1. 인증 API

### POST /api/v1/auth/register

회원가입

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "홍길동"
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "홍길동",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "created_at": "2025-01-16T00:00:00Z",
  "updated_at": "2025-01-16T00:00:00Z"
}
```

**Error (409):**
```json
{
  "error": true,
  "message": "이미 등록된 이메일입니다."
}
```

---

### POST /api/v1/auth/login

로그인

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Cookies Set:**
- `access_token` (httpOnly)
- `refresh_token` (httpOnly)

**Error (401):**
```json
{
  "error": true,
  "message": "이메일 또는 비밀번호가 올바르지 않습니다."
}
```

---

### POST /api/v1/auth/logout

로그아웃

**Response (200):**
```json
{
  "message": "로그아웃되었습니다."
}
```

**Cookies Cleared:**
- `access_token`
- `refresh_token`

---

### GET /api/v1/auth/me

현재 사용자 정보

**Headers:**
- `Cookie: access_token=...`

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "홍길동",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "created_at": "2025-01-16T00:00:00Z",
  "updated_at": "2025-01-16T00:00:00Z"
}
```

---

## 2. 아이템 API

### GET /api/v1/items

아이템 목록 조회

**Query Parameters:**
| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| skip | int | 0 | 건너뛸 개수 |
| limit | int | 20 | 조회 개수 (최대 100) |
| search | string | - | 검색어 |
| is_active | bool | - | 활성 상태 필터 |

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "아이템 제목",
    "description": "설명",
    "priority": 5,
    "is_active": true,
    "owner_id": 1,
    "created_at": "2025-01-16T00:00:00Z",
    "updated_at": "2025-01-16T00:00:00Z"
  }
]
```

---

### GET /api/v1/items/paginated

아이템 목록 조회 (페이지네이션)

**Query Parameters:**
| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| page | int | 1 | 페이지 번호 |
| size | int | 20 | 페이지 크기 |
| search | string | - | 검색어 |

**Response (200):**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

---

### GET /api/v1/items/{item_id}

아이템 상세 조회

**Response (200):**
```json
{
  "id": 1,
  "title": "아이템 제목",
  "description": "설명",
  "priority": 5,
  "is_active": true,
  "owner_id": 1,
  "created_at": "2025-01-16T00:00:00Z",
  "updated_at": "2025-01-16T00:00:00Z"
}
```

**Error (404):**
```json
{
  "error": true,
  "message": "아이템을 찾을 수 없습니다."
}
```

---

### POST /api/v1/items

아이템 생성

**Request Body:**
```json
{
  "title": "새 아이템",
  "description": "설명",
  "priority": 3
}
```

**Response (201):**
```json
{
  "id": 2,
  "title": "새 아이템",
  "description": "설명",
  "priority": 3,
  "is_active": true,
  "owner_id": 1,
  "created_at": "2025-01-16T00:00:00Z",
  "updated_at": "2025-01-16T00:00:00Z"
}
```

---

### PATCH /api/v1/items/{item_id}

아이템 수정

**Request Body:**
```json
{
  "title": "수정된 제목",
  "priority": 7
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "수정된 제목",
  "description": "설명",
  "priority": 7,
  ...
}
```

---

### DELETE /api/v1/items/{item_id}

아이템 삭제

**Response (200):**
```json
{
  "message": "아이템이 삭제되었습니다."
}
```

---

### POST /api/v1/items/{item_id}/toggle

아이템 활성/비활성 토글

**Response (200):**
```json
{
  "id": 1,
  "is_active": false,
  ...
}
```

---

## 3. HTMX 파셜 엔드포인트

### GET /partials/items

아이템 목록 파셜 (HTML)

### GET /partials/items/form

아이템 생성 폼 파셜 (HTML)

### GET /partials/items/{item_id}

단일 아이템 파셜 (HTML)

### GET /partials/items/{item_id}/edit

아이템 수정 폼 파셜 (HTML)

### POST /partials/items

아이템 생성 (HTML 응답)

**HX-Trigger Header:**
```json
{
  "showToast": {"type": "success", "message": "아이템이 생성되었습니다."},
  "closeModal": true
}
```

### PUT /partials/items/{item_id}

아이템 수정 (HTML 응답)

### DELETE /partials/items/{item_id}

아이템 삭제 (빈 HTML 응답)

---

## 4. 에러 응답

### 400 Bad Request
```json
{
  "error": true,
  "message": "잘못된 요청입니다.",
  "detail": {}
}
```

### 401 Unauthorized
```json
{
  "error": true,
  "message": "인증이 필요합니다."
}
```

### 403 Forbidden
```json
{
  "error": true,
  "message": "권한이 없습니다."
}
```

### 404 Not Found
```json
{
  "error": true,
  "message": "리소스를 찾을 수 없습니다."
}
```

### 409 Conflict
```json
{
  "error": true,
  "message": "리소스 충돌이 발생했습니다."
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "error": true,
  "message": "서버 내부 오류가 발생했습니다."
}
```

---

## 5. OpenAPI 문서

개발 모드에서 자동 생성되는 API 문서:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`
