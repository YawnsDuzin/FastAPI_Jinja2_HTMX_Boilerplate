# HTMX 가이드

## 1. HTMX 소개

HTMX는 HTML 속성만으로 AJAX, CSS Transitions, WebSocket, Server-Sent Events를 구현할 수 있게 해주는 라이브러리입니다.

### 핵심 철학
- **HTML 중심**: JavaScript 대신 HTML 속성 사용
- **서버 중심**: 서버가 HTML을 반환
- **점진적 향상**: 기본 HTML 위에 기능 추가
- **단순함**: 복잡한 프레임워크 불필요

## 2. 기본 속성

### 2.1 HTTP 요청

```html
<!-- GET 요청 -->
<button hx-get="/api/data">데이터 가져오기</button>

<!-- POST 요청 -->
<form hx-post="/api/items">
    <input name="title" type="text">
    <button type="submit">생성</button>
</form>

<!-- PUT 요청 -->
<button hx-put="/api/items/1">수정</button>

<!-- PATCH 요청 -->
<button hx-patch="/api/items/1">부분 수정</button>

<!-- DELETE 요청 -->
<button hx-delete="/api/items/1">삭제</button>
```

### 2.2 타겟 지정 (hx-target)

```html
<!-- 다른 요소에 결과 삽입 -->
<button hx-get="/partials/items"
        hx-target="#item-list">
    목록 새로고침
</button>

<div id="item-list">
    <!-- 여기에 결과가 삽입됨 -->
</div>

<!-- CSS 선택자 사용 -->
<button hx-get="/content" hx-target=".content-area">로드</button>

<!-- 가장 가까운 조상 요소 -->
<button hx-get="/content" hx-target="closest .card">로드</button>

<!-- 현재 요소 (기본값) -->
<div hx-get="/content" hx-target="this">로드</div>
```

### 2.3 스왑 방식 (hx-swap)

```html
<!-- innerHTML: 내부 HTML 교체 (기본값) -->
<div hx-get="/content" hx-swap="innerHTML">로드</div>

<!-- outerHTML: 요소 자체를 교체 -->
<div hx-get="/content" hx-swap="outerHTML">로드</div>

<!-- beforebegin: 요소 앞에 삽입 -->
<div hx-get="/content" hx-swap="beforebegin">로드</div>

<!-- afterbegin: 첫 번째 자식으로 삽입 -->
<div hx-get="/content" hx-swap="afterbegin">로드</div>

<!-- beforeend: 마지막 자식으로 삽입 -->
<div hx-get="/content" hx-swap="beforeend">로드</div>

<!-- afterend: 요소 뒤에 삽입 -->
<div hx-get="/content" hx-swap="afterend">로드</div>

<!-- delete: 요소 삭제 -->
<div hx-delete="/items/1" hx-swap="delete">삭제</div>

<!-- none: 스왑하지 않음 -->
<button hx-post="/action" hx-swap="none">실행</button>
```

### 2.4 트리거 (hx-trigger)

```html
<!-- 클릭 (기본값) -->
<button hx-get="/data" hx-trigger="click">클릭</button>

<!-- 입력 변경 -->
<input hx-get="/search" hx-trigger="change">

<!-- 키입력 (디바운스) -->
<input hx-get="/search"
       hx-trigger="keyup changed delay:300ms"
       name="q">

<!-- 폼 제출 -->
<form hx-post="/items" hx-trigger="submit">
    ...
</form>

<!-- 페이지 로드 -->
<div hx-get="/initial-data" hx-trigger="load">
    로딩 중...
</div>

<!-- 요소가 뷰포트에 들어올 때 -->
<div hx-get="/lazy-content" hx-trigger="revealed">
    지연 로딩
</div>

<!-- 인터벌 -->
<div hx-get="/live-data" hx-trigger="every 5s">
    실시간 데이터
</div>

<!-- 다중 트리거 -->
<input hx-get="/validate"
       hx-trigger="change, keyup delay:500ms changed">
```

## 3. 고급 속성

### 3.1 확인 대화상자

```html
<button hx-delete="/items/1"
        hx-confirm="정말 삭제하시겠습니까?">
    삭제
</button>
```

### 3.2 로딩 표시

```html
<!-- 로딩 인디케이터 -->
<button hx-get="/slow-data" hx-indicator="#spinner">
    데이터 로드
</button>
<span id="spinner" class="htmx-indicator">로딩 중...</span>

<!-- CSS로 스타일링 -->
<style>
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline; }
</style>
```

### 3.3 URL 히스토리

```html
<!-- URL 변경 -->
<a hx-get="/page/2" hx-push-url="true">페이지 2</a>

<!-- URL 교체 (뒤로가기 불가) -->
<a hx-get="/page/2" hx-replace-url="true">페이지 2</a>
```

### 3.4 추가 값 전송

```html
<!-- JSON 형식 -->
<button hx-post="/action"
        hx-vals='{"key": "value", "count": 1}'>
    전송
</button>

<!-- JavaScript 표현식 -->
<button hx-post="/action"
        hx-vals="js:{timestamp: Date.now()}">
    전송
</button>
```

### 3.5 헤더 설정

```html
<!-- 커스텀 헤더 -->
<button hx-get="/api/data"
        hx-headers='{"X-Custom-Header": "value"}'>
    요청
</button>
```

### 3.6 응답 일부 선택

```html
<!-- 응답에서 특정 요소만 선택 -->
<button hx-get="/full-page"
        hx-select="#content-only">
    콘텐츠만 가져오기
</button>
```

## 4. 서버 응답 헤더

### 4.1 HX-Trigger

```python
# 이벤트 트리거
response.headers["HX-Trigger"] = "itemCreated"

# 데이터와 함께
response.headers["HX-Trigger"] = json.dumps({
    "showToast": {
        "type": "success",
        "message": "저장되었습니다."
    }
})

# 여러 이벤트
response.headers["HX-Trigger"] = json.dumps({
    "closeModal": True,
    "refreshList": True,
    "showToast": {"message": "완료"}
})
```

### 4.2 기타 응답 헤더

```python
# 타겟 변경
response.headers["HX-Retarget"] = "#other-element"

# 스왑 방식 변경
response.headers["HX-Reswap"] = "outerHTML"

# 리다이렉트
response.headers["HX-Redirect"] = "/new-page"

# 새로고침
response.headers["HX-Refresh"] = "true"

# URL 변경
response.headers["HX-Push-Url"] = "/new-url"
```

## 5. 이벤트 처리

### 5.1 HTMX 이벤트

```html
<!-- 요청 전 -->
<form hx-post="/items"
      hx-on::before-request="console.log('요청 시작')">

<!-- 요청 후 -->
<form hx-post="/items"
      hx-on::after-request="if(event.detail.successful) alert('성공')">

<!-- 스왑 전 -->
<div hx-get="/content"
     hx-on::before-swap="console.log('스왑 전')">

<!-- 스왑 후 -->
<div hx-get="/content"
     hx-on::after-swap="initializeComponents()">
```

### 5.2 JavaScript 이벤트 리스닝

```javascript
// HTMX 이벤트 리스닝
document.body.addEventListener('htmx:afterRequest', (event) => {
    console.log('요청 완료:', event.detail);
});

// 커스텀 이벤트 처리
document.body.addEventListener('showToast', (event) => {
    const { type, message } = event.detail;
    showToastNotification(type, message);
});
```

## 6. 이 프로젝트의 HTMX 패턴

### 6.1 아이템 CRUD

```html
<!-- 목록 로드 -->
<div hx-get="/partials/items"
     hx-trigger="load"
     hx-swap="innerHTML">
    <p>로딩 중...</p>
</div>

<!-- 아이템 생성 -->
<form hx-post="/partials/items"
      hx-target="#item-list"
      hx-swap="afterbegin"
      hx-on::after-request="this.reset()">
    <input name="title" required>
    <button type="submit">추가</button>
</form>

<!-- 아이템 수정 -->
<button hx-get="/partials/items/{{ item.id }}/edit"
        hx-target="#modal-content"
        @click="$dispatch('openModal')">
    수정
</button>

<!-- 아이템 삭제 -->
<button hx-delete="/partials/items/{{ item.id }}"
        hx-target="#item-{{ item.id }}"
        hx-swap="outerHTML"
        hx-confirm="삭제하시겠습니까?">
    삭제
</button>
```

### 6.2 인증

```html
<!-- 로그인 폼 -->
<form hx-post="/api/v1/auth/login"
      hx-swap="none"
      hx-on::after-request="
        if(event.detail.successful) {
          window.location.href='/dashboard'
        }
      ">
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">로그인</button>
</form>

<!-- 로그아웃 -->
<button hx-post="/api/v1/auth/logout"
        hx-swap="none"
        hx-on::after-request="window.location.href='/'">
    로그아웃
</button>
```

### 6.3 검색 (디바운스)

```html
<input type="text"
       name="q"
       hx-get="/partials/items"
       hx-target="#item-list"
       hx-trigger="keyup changed delay:300ms"
       placeholder="검색...">
```

### 6.4 무한 스크롤

```html
<div id="item-list">
    {% for item in items %}
        {{ render_item(item) }}
    {% endfor %}

    {% if has_more %}
    <div hx-get="/partials/items?page={{ next_page }}"
         hx-trigger="revealed"
         hx-swap="outerHTML">
        <p>더 불러오는 중...</p>
    </div>
    {% endif %}
</div>
```

### 6.5 모달 패턴

```html
<!-- 모달 열기 -->
<button hx-get="/partials/items/form"
        hx-target="#modal-content"
        hx-swap="innerHTML"
        @click="$dispatch('openModal')">
    새 아이템
</button>

<!-- 모달 닫기 (서버에서) -->
# Python
response.headers["HX-Trigger"] = "closeModal"
```

## 7. 부스트 모드

```html
<!-- 전역 부스트 -->
<body hx-boost="true">
    <!-- 모든 링크와 폼이 AJAX로 처리됨 -->
    <a href="/about">소개</a>
</body>

<!-- 특정 요소 제외 -->
<a href="/external" hx-boost="false">외부 링크</a>
```

## 8. 디버깅

### 8.1 htmx.logAll()

```javascript
// 모든 HTMX 이벤트 로깅
htmx.logAll();
```

### 8.2 개발자 도구

- Network 탭에서 HTMX 요청 확인
- `HX-Request: true` 헤더로 HTMX 요청 식별
- 응답 HTML 미리보기

## 9. 참고 자료

- [HTMX 공식 문서](https://htmx.org/docs/)
- [HTMX 예제](https://htmx.org/examples/)
- [HTMX 참조](https://htmx.org/reference/)
