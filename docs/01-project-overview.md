# 프로젝트 개요

## 1. 프로젝트 소개

FastAPI + Jinja2 + HTMX 보일러플레이트는 모던 풀스택 웹 애플리케이션을 빠르게 개발할 수 있는 기반 코드입니다. JavaScript 프레임워크 없이 동적인 SPA-like 경험을 제공합니다.

### 핵심 철학

1. **제로 JavaScript 빌드**: npm, webpack, vite 등의 빌드 도구 없이 개발
2. **서버사이드 렌더링 우선**: SEO 친화적, 빠른 초기 로딩
3. **점진적 향상**: 기본 HTML 동작 위에 HTMX로 향상
4. **단순함**: 복잡한 상태 관리 없이 직관적인 개발

## 2. 기술 스택

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| Backend | FastAPI | 0.115+ | 비동기 웹 프레임워크 |
| Template | Jinja2 | 3.1+ | 서버사이드 렌더링 |
| Frontend | HTMX | 2.0+ | AJAX/동적 UI |
| UI Interactivity | Alpine.js | 3.x | 클라이언트 사이드 상호작용 |
| CSS | TailwindCSS | 3.4+ | 유틸리티 기반 스타일링 |
| Database | SQLAlchemy | 2.0+ | 비동기 ORM |
| Auth | python-jose | 3.3+ | JWT 인증 |

## 3. 주요 기능

### 3.1 인증 시스템
- JWT 기반 인증
- httpOnly 쿠키를 통한 토큰 저장
- 회원가입/로그인/로그아웃
- 비밀번호 변경

### 3.2 CRUD 샘플
- 아이템 생성/조회/수정/삭제
- HTMX를 통한 동적 업데이트
- 페이지네이션
- 검색 기능

### 3.3 UI 컴포넌트
- 반응형 네비게이션
- 다크 모드 지원
- 토스트 알림
- 모달 다이얼로그
- 폼 유효성 검사

## 4. 프로젝트 구조 개요

```
fastapi-htmx-boilerplate/
├── app/                    # 애플리케이션 코드
│   ├── api/               # REST API 라우터
│   ├── pages/             # HTML 페이지 라우터
│   ├── partials/          # HTMX 파셜 라우터
│   ├── models/            # SQLAlchemy 모델
│   ├── schemas/           # Pydantic 스키마
│   ├── services/          # 비즈니스 로직
│   └── core/              # 핵심 유틸리티
├── templates/             # Jinja2 템플릿
├── static/                # 정적 파일
├── tests/                 # 테스트
├── alembic/               # DB 마이그레이션
└── docs/                  # 문서
```

## 5. 왜 이 스택인가?

### HTMX의 장점
- **단순함**: HTML 속성만으로 AJAX 구현
- **서버 중심**: 비즈니스 로직이 서버에 집중
- **SEO 친화적**: 실제 HTML 콘텐츠 제공
- **유지보수 용이**: JavaScript 코드 최소화

### FastAPI의 장점
- **고성능**: Starlette 기반 비동기 처리
- **타입 안전**: Python 타입 힌트 활용
- **자동 문서화**: OpenAPI/Swagger 자동 생성
- **모던 Python**: 최신 Python 기능 활용

### Jinja2의 장점
- **강력한 템플릿**: 상속, 매크로, 필터 지원
- **보안**: 자동 XSS 방지
- **성능**: 컴파일된 템플릿
- **확장성**: 커스텀 필터/함수 추가 용이

## 6. 사용 사례

이 보일러플레이트는 다음과 같은 프로젝트에 적합합니다:

- **관리자 대시보드**: 빠른 개발, 복잡한 상호작용
- **CRUD 애플리케이션**: 데이터 관리 시스템
- **내부 도구**: 개발 시간 단축
- **MVP/프로토타입**: 빠른 검증
- **콘텐츠 관리 시스템**: SEO 중요한 사이트

## 7. 제한 사항

다음 경우에는 다른 스택을 고려하세요:

- **실시간 협업 앱**: WebSocket 중심 애플리케이션
- **복잡한 클라이언트 상태**: 많은 클라이언트 로직 필요
- **오프라인 지원**: PWA 기능 필요
- **모바일 앱**: React Native, Flutter 고려

## 8. 다음 단계

- [빠른 시작 가이드](./02-quick-start.md)로 시작하기
- [FastAPI 가이드](./03-fastapi-guide.md)로 백엔드 이해하기
- [HTMX 가이드](./05-htmx-guide.md)로 동적 UI 구현하기
