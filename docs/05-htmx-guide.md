# HTMX 가이드

## 1. HTMX란 무엇인가?

### 1.1 기본 개념

HTMX는 **HTML 속성만으로 AJAX 요청을 보내고 페이지 일부를 업데이트**할 수 있게 해주는 JavaScript 라이브러리입니다.

**일반 웹 vs HTMX:**
```
[일반 웹 페이지]
사용자 클릭 → 전체 페이지 새로고침 → 전체 HTML 다시 받음 → 화면 깜빡임

[HTMX 사용]
사용자 클릭 → 필요한 부분만 요청 → 작은 HTML 조각 받음 → 해당 부분만 업데이트
```

**왜 HTMX를 사용하는가?**

| 비교 항목 | React/Vue | HTMX |
|----------|-----------|------|
| 학습 난이도 | 높음 (JavaScript 필수) | 낮음 (HTML만 알면 됨) |
| 서버 응답 | JSON | HTML |
| 상태 관리 | 클라이언트 (복잡) | 서버 (단순) |
| 번들 크기 | 수백 KB | ~14KB |
| SEO | 추가 작업 필요 | 기본 지원 |

### 1.2 핵심 철학

```
기존 SPA (React, Vue):
서버 → JSON 데이터 → 클라이언트에서 HTML 생성 → 렌더링

HTMX:
서버 → HTML 조각 → 그대로 페이지에 삽입 → 렌더링

HTMX의 모토:
"왜 브라우저가 HTML을 렌더링하는데,
 JSON을 보내고 클라이언트에서 다시 HTML로 바꾸는가?"
```

---

## 2. 기본 속성 이해하기

### 2.1 hx-get, hx-post, hx-put, hx-delete

HTTP 요청을 보내는 가장 기본적인 속성들입니다.

```html
<!-- ================================================================== -->
<!-- hx-get: GET 요청 (데이터 조회)                                     -->
<!-- ================================================================== -->

<button hx-get="/api/users">
    사용자 목록 가져오기
</button>
<!--
    동작:
    1. 버튼을 클릭하면
    2. GET /api/users 요청을 보내고
    3. 응답으로 받은 HTML을 이 버튼 안에 삽입

    일반 JavaScript로 하면:
    button.onclick = async () => {
        const response = await fetch('/api/users');
        const html = await response.text();
        button.innerHTML = html;
    }

    HTMX로는 속성 하나로 끝!
-->


<!-- ================================================================== -->
<!-- hx-post: POST 요청 (데이터 생성)                                   -->
<!-- ================================================================== -->

<form hx-post="/api/users">
    <input name="username" type="text" placeholder="사용자명">
    <input name="email" type="email" placeholder="이메일">
    <button type="submit">회원가입</button>
</form>
<!--
    동작:
    1. 폼을 제출하면
    2. POST /api/users 요청을 보냄
    3. input 값들이 자동으로 폼 데이터로 전송됨
    4. 응답 HTML이 <form> 안에 삽입됨

    전통적인 폼과의 차이:
    - 전통적 폼: 전체 페이지가 새로고침됨
    - HTMX 폼: 페이지 새로고침 없이 부분 업데이트
-->


<!-- ================================================================== -->
<!-- hx-put: PUT 요청 (데이터 전체 수정)                                -->
<!-- ================================================================== -->

<form hx-put="/api/users/1">
    <input name="username" type="text" value="현재 이름">
    <input name="email" type="email" value="현재 이메일">
    <button type="submit">수정</button>
</form>
<!--
    동작:
    1. 폼을 제출하면
    2. PUT /api/users/1 요청을 보냄
    3. 1번 사용자의 정보를 전체 업데이트
-->


<!-- ================================================================== -->
<!-- hx-patch: PATCH 요청 (데이터 일부 수정)                            -->
<!-- ================================================================== -->

<button hx-patch="/api/users/1" hx-vals='{"status": "active"}'>
    활성화
</button>
<!--
    동작:
    1. 버튼을 클릭하면
    2. PATCH /api/users/1 요청을 보냄
    3. status 필드만 "active"로 변경
-->


<!-- ================================================================== -->
<!-- hx-delete: DELETE 요청 (데이터 삭제)                               -->
<!-- ================================================================== -->

<button hx-delete="/api/users/1">
    삭제
</button>
<!--
    동작:
    1. 버튼을 클릭하면
    2. DELETE /api/users/1 요청을 보냄
    3. 1번 사용자 삭제
-->
```

### 2.2 hx-target (응답을 어디에 넣을지)

기본적으로 응답은 요청을 보낸 요소 안에 삽입됩니다. `hx-target`으로 다른 위치를 지정할 수 있습니다.

```html
<!-- ================================================================== -->
<!-- 기본 동작: 요청을 보낸 요소 안에 삽입                               -->
<!-- ================================================================== -->

<button hx-get="/partials/content">
    내용 로드
</button>
<!--
    결과:
    <button hx-get="/partials/content">
        [서버 응답 HTML이 여기에 들어감]
    </button>
-->


<!-- ================================================================== -->
<!-- hx-target: 다른 요소에 삽입                                        -->
<!-- ================================================================== -->

<button hx-get="/partials/users"
        hx-target="#user-list">
    사용자 목록 새로고침
</button>

<div id="user-list">
    <!-- 여기에 응답 HTML이 들어감 -->
</div>
<!--
    hx-target="#user-list"
    → CSS 선택자로 타겟 요소 지정
    → 응답이 id="user-list"인 요소에 삽입됨

    지원하는 선택자:
    - #id: ID로 선택
    - .class: 클래스로 선택
    - 태그명: 태그로 선택
-->


<!-- ================================================================== -->
<!-- 특수 타겟 값들                                                      -->
<!-- ================================================================== -->

<!-- this: 현재 요소 (기본값) -->
<div hx-get="/content" hx-target="this">
    로드
</div>

<!-- closest: 가장 가까운 조상 요소 -->
<tr>
    <td>홍길동</td>
    <td>
        <button hx-delete="/users/1"
                hx-target="closest tr">
            삭제
        </button>
        <!-- 삭제 시 이 버튼의 부모 <tr>이 타겟이 됨 -->
    </td>
</tr>

<!-- find: 자손 요소에서 찾기 -->
<div hx-get="/content" hx-target="find .content">
    <div class="content">여기에 삽입됨</div>
</div>

<!-- next/previous: 형제 요소 -->
<button hx-get="/content" hx-target="next div">
    다음 div에 로드
</button>
<div>여기에 삽입됨</div>
```

### 2.3 hx-swap (어떻게 교체할지)

응답 HTML을 타겟에 어떻게 삽입할지 결정합니다.

```html
<!-- ================================================================== -->
<!-- innerHTML (기본값): 내부 HTML을 교체                               -->
<!-- ================================================================== -->

<div id="container" hx-get="/content" hx-swap="innerHTML">
    <p>이 내용이</p>
</div>
<!--
    서버 응답: <p>새 내용</p>

    결과:
    <div id="container">
        <p>새 내용</p>   ← 내부 내용만 교체됨
    </div>
-->


<!-- ================================================================== -->
<!-- outerHTML: 요소 자체를 교체                                        -->
<!-- ================================================================== -->

<div id="old-element" hx-get="/content" hx-swap="outerHTML">
    내용
</div>
<!--
    서버 응답: <div id="new-element">새 요소</div>

    결과:
    <div id="new-element">새 요소</div>  ← 요소 자체가 교체됨

    주의: 기존 요소(#old-element)가 완전히 사라짐!
-->


<!-- ================================================================== -->
<!-- beforebegin: 요소 앞에 삽입                                        -->
<!-- ================================================================== -->

<div id="reference" hx-get="/content" hx-swap="beforebegin">
    기준 요소
</div>
<!--
    서버 응답: <p>새 내용</p>

    결과:
    <p>새 내용</p>        ← 앞에 삽입됨
    <div id="reference">
        기준 요소
    </div>
-->


<!-- ================================================================== -->
<!-- afterbegin: 첫 번째 자식으로 삽입                                  -->
<!-- ================================================================== -->

<ul id="list" hx-get="/new-item" hx-swap="afterbegin">
    <li>기존 항목 1</li>
    <li>기존 항목 2</li>
</ul>
<!--
    서버 응답: <li>새 항목</li>

    결과:
    <ul id="list">
        <li>새 항목</li>        ← 맨 앞에 추가됨
        <li>기존 항목 1</li>
        <li>기존 항목 2</li>
    </ul>
-->


<!-- ================================================================== -->
<!-- beforeend: 마지막 자식으로 삽입                                    -->
<!-- ================================================================== -->

<ul id="list" hx-get="/new-item" hx-swap="beforeend">
    <li>기존 항목 1</li>
    <li>기존 항목 2</li>
</ul>
<!--
    서버 응답: <li>새 항목</li>

    결과:
    <ul id="list">
        <li>기존 항목 1</li>
        <li>기존 항목 2</li>
        <li>새 항목</li>        ← 맨 뒤에 추가됨
    </ul>

    활용: 무한 스크롤에서 새 아이템 추가할 때 유용
-->


<!-- ================================================================== -->
<!-- afterend: 요소 뒤에 삽입                                           -->
<!-- ================================================================== -->

<div id="reference" hx-get="/content" hx-swap="afterend">
    기준 요소
</div>
<!--
    서버 응답: <p>새 내용</p>

    결과:
    <div id="reference">
        기준 요소
    </div>
    <p>새 내용</p>        ← 뒤에 삽입됨
-->


<!-- ================================================================== -->
<!-- delete: 타겟 요소 삭제 (응답 무시)                                 -->
<!-- ================================================================== -->

<div id="item-1" hx-delete="/items/1" hx-swap="delete">
    <p>삭제할 아이템</p>
    <button>삭제</button>
</div>
<!--
    버튼 클릭 시:
    1. DELETE /items/1 요청
    2. 응답과 관계없이 #item-1 요소가 DOM에서 제거됨

    결과:
    (요소가 완전히 사라짐)
-->


<!-- ================================================================== -->
<!-- none: 아무것도 하지 않음 (응답 무시)                               -->
<!-- ================================================================== -->

<button hx-post="/api/action" hx-swap="none">
    실행
</button>
<!--
    동작:
    1. POST /api/action 요청
    2. 응답을 받지만 DOM에 아무 변화 없음

    활용: 서버 액션만 필요하고 UI 업데이트가 필요 없을 때
    (예: 로그 기록, 통계 전송 등)
-->


<!-- ================================================================== -->
<!-- swap 수식어 (modifiers)                                            -->
<!-- ================================================================== -->

<!-- 스왑 후 스크롤 -->
<div hx-get="/content" hx-swap="innerHTML scroll:top">
    <!-- 스왑 후 맨 위로 스크롤 -->
</div>

<!-- 스왑 애니메이션 타이밍 -->
<div hx-get="/content" hx-swap="innerHTML swap:1s">
    <!-- 1초에 걸쳐 스왑 애니메이션 -->
</div>

<!-- 정착 시간 -->
<div hx-get="/content" hx-swap="innerHTML settle:500ms">
    <!-- CSS 트랜지션을 위해 500ms 대기 -->
</div>
```

### 2.4 hx-trigger (언제 요청을 보낼지)

요청을 보내는 시점을 결정합니다.

```html
<!-- ================================================================== -->
<!-- click (기본값): 클릭 시                                            -->
<!-- ================================================================== -->

<button hx-get="/content" hx-trigger="click">
    클릭하면 요청
</button>
<!--
    hx-trigger를 생략하면 기본값은:
    - 버튼, 링크: click
    - 폼: submit
    - input, select, textarea: change
-->


<!-- ================================================================== -->
<!-- change: 값이 변경될 때                                             -->
<!-- ================================================================== -->

<select hx-get="/filter" hx-trigger="change" name="category">
    <option value="all">전체</option>
    <option value="food">음식</option>
    <option value="tech">기술</option>
</select>
<!--
    동작:
    1. 선택 값이 바뀌면
    2. GET /filter?category=선택값 요청
-->


<!-- ================================================================== -->
<!-- keyup: 키보드 입력 시                                              -->
<!-- ================================================================== -->

<input type="text"
       hx-get="/search"
       hx-trigger="keyup"
       hx-target="#results"
       name="q"
       placeholder="검색...">

<div id="results">
    <!-- 검색 결과가 여기에 표시됨 -->
</div>
<!--
    동작:
    1. 키보드를 누를 때마다
    2. GET /search?q=입력값 요청
    3. 결과가 #results에 표시됨

    문제: 매 키 입력마다 요청이 가서 서버에 부담!
-->


<!-- ================================================================== -->
<!-- keyup + delay: 디바운스 (입력 후 대기)                             -->
<!-- ================================================================== -->

<input type="text"
       hx-get="/search"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#results"
       name="q">
<!--
    hx-trigger="keyup changed delay:300ms"

    분석:
    - keyup: 키를 놓을 때
    - changed: 값이 실제로 변경되었을 때만
    - delay:300ms: 300ms 동안 추가 입력이 없으면 요청

    동작:
    1. 사용자가 "hello" 입력
    2. h → e → l → l → o (각 키 입력 시 타이머 리셋)
    3. 마지막 'o' 입력 후 300ms 대기
    4. 추가 입력 없으면 GET /search?q=hello 요청

    이렇게 하면 서버 요청 횟수가 크게 줄어듦!
-->


<!-- ================================================================== -->
<!-- load: 페이지/요소 로드 시                                          -->
<!-- ================================================================== -->

<div hx-get="/dashboard/stats"
     hx-trigger="load"
     hx-swap="innerHTML">
    <p>통계 로딩 중...</p>
</div>
<!--
    동작:
    1. 이 div가 DOM에 나타나면
    2. 즉시 GET /dashboard/stats 요청
    3. 응답으로 "로딩 중..." 교체

    활용: 페이지 로드 시 데이터를 비동기로 가져올 때
-->


<!-- ================================================================== -->
<!-- revealed: 요소가 뷰포트에 보일 때 (지연 로딩)                      -->
<!-- ================================================================== -->

<div hx-get="/lazy-content"
     hx-trigger="revealed"
     hx-swap="outerHTML">
    <p>스크롤하면 로드됩니다...</p>
</div>
<!--
    동작:
    1. 처음에는 아무것도 안 함
    2. 사용자가 스크롤해서 이 요소가 화면에 보이면
    3. GET /lazy-content 요청

    활용:
    - 이미지 지연 로딩
    - 무한 스크롤
    - 성능 최적화
-->


<!-- ================================================================== -->
<!-- every: 주기적으로 (폴링)                                           -->
<!-- ================================================================== -->

<div hx-get="/notifications"
     hx-trigger="every 5s"
     hx-swap="innerHTML">
    <!-- 5초마다 알림 업데이트 -->
</div>
<!--
    동작:
    1. 5초마다 GET /notifications 요청
    2. 응답으로 내용 업데이트

    활용:
    - 실시간 알림 (WebSocket 대안)
    - 라이브 데이터 표시
    - 채팅 앱
-->


<!-- ================================================================== -->
<!-- 복합 트리거                                                         -->
<!-- ================================================================== -->

<input type="text"
       hx-get="/validate"
       hx-trigger="change, keyup delay:500ms changed">
<!--
    여러 트리거를 콤마로 연결

    동작:
    - 포커스를 벗어나면 (change) 즉시 검증
    - 키 입력 시 (keyup) 500ms 후 검증
-->


<!-- ================================================================== -->
<!-- 이벤트 필터                                                         -->
<!-- ================================================================== -->

<input type="text"
       hx-get="/search"
       hx-trigger="keyup[key=='Enter']">
<!--
    조건부 트리거: Enter 키를 눌렀을 때만 요청

    [] 안에 JavaScript 조건식 사용
    event 객체의 속성에 접근 가능
-->


<!-- ================================================================== -->
<!-- from: 다른 요소의 이벤트 감지                                      -->
<!-- ================================================================== -->

<input type="text" id="search-input" name="q">

<div hx-get="/search"
     hx-trigger="keyup changed delay:300ms from:#search-input"
     hx-include="#search-input">
    <!-- #search-input의 keyup 이벤트를 감지 -->
</div>
<!--
    from:#search-input
    → #search-input 요소의 이벤트를 감지

    활용: 입력 필드와 결과 영역이 떨어져 있을 때
-->
```

---

## 3. 추가 요청 데이터

### 3.1 hx-vals (추가 값 전송)

```html
<!-- ================================================================== -->
<!-- JSON 형식으로 추가 값 전송                                         -->
<!-- ================================================================== -->

<button hx-post="/api/action"
        hx-vals='{"type": "delete", "force": true}'>
    삭제
</button>
<!--
    hx-vals='JSON 문자열'
    → 요청에 추가 데이터 포함

    전송되는 데이터:
    type=delete
    force=true

    주의: 작은따옴표와 큰따옴표 순서에 주의!
    hx-vals='{"key": "value"}'  ← 올바름
    hx-vals="{'key': 'value'}"  ← 오류!
-->


<!-- ================================================================== -->
<!-- JavaScript 표현식 사용                                             -->
<!-- ================================================================== -->

<button hx-post="/api/log"
        hx-vals="js:{timestamp: Date.now(), path: window.location.pathname}">
    로그 기록
</button>
<!--
    hx-vals="js:{...}"
    → JavaScript 표현식 실행 결과를 전송

    전송되는 데이터:
    timestamp=1705312345678
    path=/dashboard
-->
```

### 3.2 hx-include (다른 요소 값 포함)

```html
<!-- ================================================================== -->
<!-- 특정 입력 필드 포함                                                -->
<!-- ================================================================== -->

<input type="text" id="search-query" name="q" value="hello">

<button hx-get="/search"
        hx-include="#search-query">
    검색
</button>
<!--
    hx-include="#search-query"
    → #search-query의 값을 요청에 포함

    요청: GET /search?q=hello
-->


<!-- ================================================================== -->
<!-- 여러 요소 포함                                                     -->
<!-- ================================================================== -->

<input type="text" name="keyword" id="keyword">
<select name="category" id="category">
    <option value="all">전체</option>
    <option value="food">음식</option>
</select>

<button hx-get="/filter"
        hx-include="#keyword, #category">
    필터
</button>
<!--
    여러 요소를 콤마로 구분

    요청: GET /filter?keyword=검색어&category=food
-->


<!-- ================================================================== -->
<!-- 클래스로 포함                                                      -->
<!-- ================================================================== -->

<input class="filter-input" name="min_price" value="1000">
<input class="filter-input" name="max_price" value="5000">
<select class="filter-input" name="sort">
    <option value="price">가격순</option>
</select>

<button hx-get="/products"
        hx-include=".filter-input">
    적용
</button>
<!--
    .filter-input 클래스를 가진 모든 요소의 값 포함

    요청: GET /products?min_price=1000&max_price=5000&sort=price
-->
```

---

## 4. 사용자 경험 (UX) 속성

### 4.1 hx-confirm (확인 대화상자)

```html
<!-- ================================================================== -->
<!-- 삭제 전 확인                                                       -->
<!-- ================================================================== -->

<button hx-delete="/items/1"
        hx-confirm="정말 삭제하시겠습니까?&#10;이 작업은 되돌릴 수 없습니다.">
    삭제
</button>
<!--
    hx-confirm="메시지"
    → 요청 전 확인 대화상자 표시
    → 확인 클릭 시 요청 진행
    → 취소 클릭 시 요청 취소

    &#10; → 줄바꿈 문자
-->
```

### 4.2 hx-indicator (로딩 표시)

```html
<!-- ================================================================== -->
<!-- 기본 로딩 인디케이터                                               -->
<!-- ================================================================== -->

<button hx-get="/slow-data"
        hx-indicator="#loading">
    데이터 로드
</button>

<span id="loading" class="htmx-indicator">
    로딩 중...
</span>

<style>
/* HTMX 기본 인디케이터 스타일 */
.htmx-indicator {
    display: none;  /* 기본적으로 숨김 */
}

/* 요청 중일 때 표시 */
.htmx-request .htmx-indicator {
    display: inline;
}

/* 또는 */
.htmx-request.htmx-indicator {
    display: inline;
}
</style>
<!--
    동작:
    1. 버튼 클릭
    2. .htmx-request 클래스가 버튼에 추가됨
    3. #loading이 표시됨
    4. 응답 받으면 .htmx-request 제거
    5. #loading이 숨겨짐
-->


<!-- ================================================================== -->
<!-- 스피너 애니메이션                                                   -->
<!-- ================================================================== -->

<button hx-get="/data" hx-indicator=".spinner">
    <span class="btn-text">로드</span>
    <span class="spinner htmx-indicator">
        <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <!-- 스피너 SVG -->
        </svg>
    </span>
</button>


<!-- ================================================================== -->
<!-- 버튼 비활성화                                                       -->
<!-- ================================================================== -->

<button hx-get="/data"
        hx-disabled-elt="this">
    로드
</button>
<!--
    hx-disabled-elt="this"
    → 요청 중 버튼 비활성화
    → 중복 클릭 방지
-->
```

### 4.3 hx-push-url (URL 변경)

```html
<!-- ================================================================== -->
<!-- 브라우저 히스토리에 URL 추가                                       -->
<!-- ================================================================== -->

<a hx-get="/page/2"
   hx-target="#content"
   hx-push-url="true">
    2페이지
</a>
<!--
    hx-push-url="true"
    → 브라우저 주소창이 /page/2로 변경됨
    → 뒤로가기 버튼으로 이전 페이지로 돌아갈 수 있음

    동작:
    1. 클릭
    2. GET /page/2 요청
    3. 응답을 #content에 삽입
    4. 주소창이 /page/2로 변경
-->


<!-- ================================================================== -->
<!-- 특정 URL로 변경                                                    -->
<!-- ================================================================== -->

<a hx-get="/api/products?page=2"
   hx-push-url="/products?page=2">
    2페이지
</a>
<!--
    API URL과 표시 URL이 다를 때 유용
    → 요청: /api/products?page=2
    → 주소창: /products?page=2
-->


<!-- ================================================================== -->
<!-- URL 교체 (히스토리 없음)                                           -->
<!-- ================================================================== -->

<a hx-get="/page/2"
   hx-replace-url="true">
    2페이지
</a>
<!--
    hx-replace-url="true"
    → 현재 URL을 교체 (히스토리에 추가 안 함)
    → 뒤로가기로 돌아갈 수 없음
-->
```

---

## 5. 서버 응답 헤더

서버에서 응답 헤더를 통해 HTMX의 동작을 제어할 수 있습니다.

### 5.1 HX-Trigger (이벤트 발생)

```python
# FastAPI 예제

from fastapi import Response
import json

@app.post("/items")
async def create_item(response: Response):
    # 아이템 생성 로직...

    # ================================================================
    # 단순 이벤트 발생
    # ================================================================
    response.headers["HX-Trigger"] = "itemCreated"
    # → 클라이언트에서 "itemCreated" 이벤트 발생

    return "<p>아이템 생성됨</p>"
```

```html
<!-- 이벤트 수신 -->
<div hx-trigger="itemCreated from:body">
    <!-- itemCreated 이벤트가 발생하면 새로고침 -->
</div>

<!-- JavaScript로 이벤트 처리 -->
<script>
document.body.addEventListener('itemCreated', function(event) {
    console.log('아이템이 생성되었습니다!');
});
</script>
```

```python
# ================================================================
# 데이터와 함께 이벤트 발생
# ================================================================

@app.post("/items")
async def create_item(response: Response):
    response.headers["HX-Trigger"] = json.dumps({
        "showToast": {
            "type": "success",
            "message": "아이템이 생성되었습니다!"
        }
    })
    return ""
```

```html
<!-- 데이터와 함께 이벤트 수신 -->
<script>
document.body.addEventListener('showToast', function(event) {
    const { type, message } = event.detail;
    // type: "success"
    // message: "아이템이 생성되었습니다!"

    showToastNotification(type, message);
});
</script>
```

```python
# ================================================================
# 여러 이벤트 발생
# ================================================================

@app.delete("/items/{id}")
async def delete_item(response: Response):
    response.headers["HX-Trigger"] = json.dumps({
        "closeModal": True,       # 모달 닫기
        "refreshList": True,      # 목록 새로고침
        "showToast": {            # 토스트 표시
            "message": "삭제됨"
        }
    })
    return ""
```

### 5.2 다른 응답 헤더들

```python
# ================================================================
# HX-Retarget: 응답을 다른 요소에 삽입
# ================================================================

@app.post("/items")
async def create_item(response: Response):
    response.headers["HX-Retarget"] = "#item-list"
    # → 원래 타겟 무시하고 #item-list에 삽입
    return "<li>새 아이템</li>"


# ================================================================
# HX-Reswap: 스왑 방식 변경
# ================================================================

@app.post("/items")
async def create_item(response: Response):
    response.headers["HX-Reswap"] = "beforeend"
    # → innerHTML 대신 beforeend로 스왑
    return "<li>새 아이템</li>"


# ================================================================
# HX-Redirect: 페이지 이동
# ================================================================

@app.post("/login")
async def login(response: Response):
    # 로그인 성공 후 대시보드로 이동
    response.headers["HX-Redirect"] = "/dashboard"
    return ""
# → 클라이언트가 /dashboard로 전체 페이지 이동


# ================================================================
# HX-Refresh: 페이지 새로고침
# ================================================================

@app.post("/settings")
async def save_settings(response: Response):
    response.headers["HX-Refresh"] = "true"
    return ""
# → 전체 페이지 새로고침


# ================================================================
# HX-Push-Url: URL 변경
# ================================================================

@app.get("/search")
async def search(response: Response, q: str):
    response.headers["HX-Push-Url"] = f"/search?q={q}"
    return render_search_results(q)
# → 브라우저 주소창 변경
```

---

## 6. 이벤트 처리

### 6.1 HTMX 이벤트

```html
<!-- ================================================================== -->
<!-- hx-on:: 인라인 이벤트 핸들러                                       -->
<!-- ================================================================== -->

<!-- 요청 전 -->
<form hx-post="/items"
      hx-on::before-request="console.log('요청 시작!')">
    ...
</form>
<!--
    hx-on::이벤트명="JavaScript 코드"
    → 해당 이벤트 발생 시 JavaScript 실행
-->


<!-- 요청 성공 후 -->
<form hx-post="/items"
      hx-on::after-request="if(event.detail.successful) this.reset()">
    <input name="title">
    <button type="submit">추가</button>
</form>
<!--
    event.detail.successful: 요청 성공 여부
    this: 이벤트가 발생한 요소 (form)
    this.reset(): 폼 초기화
-->


<!-- 스왑 후 -->
<div hx-get="/content"
     hx-on::after-swap="initializeComponents()">
    ...
</div>
<!--
    스왑이 완료된 후 JavaScript 함수 호출
    → 새로 추가된 요소 초기화에 유용
-->


<!-- 에러 처리 -->
<button hx-get="/api/data"
        hx-on::response-error="alert('에러 발생: ' + event.detail.xhr.status)">
    로드
</button>
```

### 6.2 JavaScript에서 이벤트 처리

```javascript
// ================================================================
// 전역 이벤트 리스너
// ================================================================

// 모든 HTMX 요청 전
document.body.addEventListener('htmx:beforeRequest', function(event) {
    console.log('요청 시작:', event.detail.pathInfo.requestPath);

    // event.detail 객체:
    // - elt: 요청을 보낸 요소
    // - xhr: XMLHttpRequest 객체
    // - target: 타겟 요소
    // - requestConfig: 요청 설정
});


// 모든 HTMX 요청 후
document.body.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.successful) {
        console.log('요청 성공!');
    } else {
        console.log('요청 실패:', event.detail.xhr.status);
    }
});


// 스왑 전
document.body.addEventListener('htmx:beforeSwap', function(event) {
    // 응답 내용 수정 가능
    console.log('스왑 전 응답:', event.detail.serverResponse);
});


// 스왑 후
document.body.addEventListener('htmx:afterSwap', function(event) {
    console.log('스왑 완료!');

    // 새로 추가된 요소에 대한 초기화
    initializeDatePickers();
    initializeTooltips();
});


// ================================================================
// 커스텀 이벤트 처리 (서버에서 HX-Trigger로 발생)
// ================================================================

document.body.addEventListener('showToast', function(event) {
    const { type, message } = event.detail;

    // 토스트 알림 표시
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.getElementById('toast-container').appendChild(toast);

    // 5초 후 제거
    setTimeout(() => toast.remove(), 5000);
});


document.body.addEventListener('closeModal', function(event) {
    document.getElementById('modal').classList.add('hidden');
});


document.body.addEventListener('refreshList', function(event) {
    // 목록 강제 새로고침
    htmx.trigger('#item-list', 'revealed');
});
```

---

## 7. 이 프로젝트의 HTMX 패턴

### 7.1 아이템 CRUD

```html
<!-- ================================================================== -->
<!-- 아이템 목록 페이지 (templates/pages/items.html)                    -->
<!-- ================================================================== -->

{% extends "base.html" %}

{% block content %}
<div class="container mx-auto">
    <h1>내 아이템</h1>

    <!-- 아이템 생성 폼 -->
    <form hx-post="/partials/items"
          hx-target="#item-list"
          hx-swap="afterbegin"
          hx-on::after-request="if(event.detail.successful) this.reset()">
        <!--
            hx-post="/partials/items"
            → POST 요청으로 새 아이템 생성

            hx-target="#item-list"
            → 응답을 아이템 목록에 삽입

            hx-swap="afterbegin"
            → 목록 맨 앞에 추가

            hx-on::after-request="..."
            → 성공 시 폼 초기화
        -->
        <input name="title" placeholder="제목" required>
        <button type="submit">추가</button>
    </form>

    <!-- 아이템 목록 (초기 로드) -->
    <div id="item-list"
         hx-get="/partials/items"
         hx-trigger="load">
        <!--
            hx-trigger="load"
            → 페이지 로드 시 자동으로 목록 가져옴
        -->
        <p>로딩 중...</p>
    </div>
</div>
{% endblock %}
```

```html
<!-- ================================================================== -->
<!-- 아이템 목록 파셜 (templates/partials/items/list.html)              -->
<!-- ================================================================== -->

{% for item in items %}
<div id="item-{{ item.id }}" class="item-card">
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>

    <div class="actions">
        <!-- 수정 버튼 -->
        <button hx-get="/partials/items/{{ item.id }}/edit"
                hx-target="#modal-content"
                @click="$dispatch('openModal')">
            <!--
                hx-get="/partials/items/1/edit"
                → 수정 폼 가져오기

                hx-target="#modal-content"
                → 모달에 삽입

                @click="$dispatch('openModal')"
                → Alpine.js로 모달 열기
            -->
            수정
        </button>

        <!-- 삭제 버튼 -->
        <button hx-delete="/partials/items/{{ item.id }}"
                hx-target="#item-{{ item.id }}"
                hx-swap="outerHTML"
                hx-confirm="정말 삭제하시겠습니까?">
            <!--
                hx-delete="/partials/items/1"
                → 삭제 요청

                hx-target="#item-1"
                → 이 아이템 카드를 타겟

                hx-swap="outerHTML"
                → 응답(빈 HTML)으로 카드 자체 교체
                → 결과적으로 카드가 사라짐

                hx-confirm="..."
                → 삭제 전 확인
            -->
            삭제
        </button>
    </div>
</div>
{% else %}
<p class="empty">아이템이 없습니다.</p>
{% endfor %}
```

```python
# ================================================================
# 서버 측 파셜 라우터 (app/partials/items.py)
# ================================================================

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import json

router = APIRouter(prefix="/partials/items")

# 아이템 목록
@router.get("", response_class=HTMLResponse)
async def get_items(request: Request, db: DbSession, user: CurrentUser):
    items = await item_service.get_all(db, user.id)
    return templates.TemplateResponse(
        request=request,
        name="partials/items/list.html",
        context={"items": items}
    )


# 아이템 생성
@router.post("", response_class=HTMLResponse)
async def create_item(
    request: Request,
    item: ItemCreate,
    db: DbSession,
    user: CurrentUser
):
    new_item = await item_service.create(db, item, user.id)

    # 성공 토스트 트리거
    response = templates.TemplateResponse(
        request=request,
        name="partials/items/item.html",
        context={"item": new_item}
    )
    response.headers["HX-Trigger"] = json.dumps({
        "showToast": {"type": "success", "message": "아이템이 생성되었습니다!"}
    })
    return response


# 아이템 삭제
@router.delete("/{item_id}", response_class=HTMLResponse)
async def delete_item(item_id: int, db: DbSession, user: CurrentUser):
    await item_service.delete(db, item_id, user.id)

    # 빈 응답 + 토스트 트리거
    response = HTMLResponse(content="")  # 빈 HTML → 아이템 카드 삭제됨
    response.headers["HX-Trigger"] = json.dumps({
        "showToast": {"type": "success", "message": "아이템이 삭제되었습니다!"}
    })
    return response
```

### 7.2 검색 (디바운스)

```html
<!-- ================================================================== -->
<!-- 실시간 검색                                                         -->
<!-- ================================================================== -->

<div class="search-container">
    <input type="text"
           name="q"
           hx-get="/partials/items"
           hx-target="#item-list"
           hx-trigger="keyup changed delay:300ms"
           hx-indicator="#search-spinner"
           placeholder="검색...">
    <!--
        hx-get="/partials/items"
        → 검색 요청 (name="q"의 값이 자동 포함됨)
        → GET /partials/items?q=검색어

        hx-trigger="keyup changed delay:300ms"
        → 키 입력 후 300ms 대기
        → 디바운스로 서버 부하 감소

        hx-indicator="#search-spinner"
        → 검색 중 스피너 표시
    -->

    <span id="search-spinner" class="htmx-indicator">
        검색 중...
    </span>
</div>

<div id="item-list">
    <!-- 검색 결과가 여기에 표시됨 -->
</div>
```

### 7.3 무한 스크롤

```html
<!-- ================================================================== -->
<!-- 무한 스크롤 구현                                                    -->
<!-- ================================================================== -->

<div id="item-list">
    {% for item in items %}
    <div class="item">{{ item.title }}</div>
    {% endfor %}

    {% if has_more %}
    <!-- 더 보기 트리거 -->
    <div hx-get="/partials/items?page={{ next_page }}"
         hx-trigger="revealed"
         hx-swap="outerHTML"
         class="loading-trigger">
        <!--
            hx-trigger="revealed"
            → 이 요소가 화면에 보이면 요청

            hx-swap="outerHTML"
            → 이 요소를 응답으로 교체
            → 응답에 다음 아이템들 + 새로운 트리거가 포함됨
        -->
        <p>더 불러오는 중...</p>
    </div>
    {% endif %}
</div>
```

```python
# 서버 측
@router.get("/partials/items")
async def get_items(request: Request, page: int = 1):
    items = await get_items_page(page)
    has_more = len(items) == PAGE_SIZE

    return templates.TemplateResponse(
        request=request,
        name="partials/items/page.html",
        context={
            "items": items,
            "has_more": has_more,
            "next_page": page + 1
        }
    )
```

### 7.4 모달 패턴

```html
<!-- ================================================================== -->
<!-- 모달 컨테이너 (base.html)                                          -->
<!-- ================================================================== -->

<div id="modal-container"
     x-data="{ open: false }"
     @openModal.window="open = true"
     @closeModal.window="open = false"
     @keydown.escape.window="open = false">

    <!-- 배경 -->
    <div x-show="open"
         class="fixed inset-0 bg-black/50"
         @click="open = false">
    </div>

    <!-- 모달 내용 -->
    <div id="modal-content"
         x-show="open"
         class="fixed inset-0 flex items-center justify-center">
        <!-- HTMX가 여기에 내용 삽입 -->
    </div>
</div>


<!-- ================================================================== -->
<!-- 모달 열기 버튼                                                      -->
<!-- ================================================================== -->

<button hx-get="/partials/items/1/edit"
        hx-target="#modal-content"
        hx-swap="innerHTML"
        @click="$dispatch('openModal')">
    수정
</button>
<!--
    동작:
    1. 클릭
    2. GET /partials/items/1/edit 요청
    3. 응답을 #modal-content에 삽입
    4. Alpine.js 이벤트로 모달 열기
-->


<!-- ================================================================== -->
<!-- 모달 내용 (서버 응답)                                               -->
<!-- ================================================================== -->

<div class="bg-white p-6 rounded-lg shadow-xl">
    <h2>아이템 수정</h2>

    <form hx-put="/partials/items/1"
          hx-swap="none">
        <input name="title" value="{{ item.title }}">
        <button type="submit">저장</button>
        <button type="button" @click="$dispatch('closeModal')">
            취소
        </button>
    </form>
</div>
```

```python
# 서버에서 모달 닫기
@router.put("/partials/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate):
    await item_service.update(item_id, item)

    response = HTMLResponse(content="")
    response.headers["HX-Trigger"] = json.dumps({
        "closeModal": True,
        "refreshList": True,
        "showToast": {"type": "success", "message": "수정되었습니다!"}
    })
    return response
```

---

## 8. hx-boost (전역 부스트)

```html
<!-- ================================================================== -->
<!-- 전역 부스트 활성화                                                  -->
<!-- ================================================================== -->

<body hx-boost="true">
    <!--
        hx-boost="true"
        → 모든 <a>와 <form>이 HTMX로 처리됨
        → 전체 페이지 새로고침 없이 body만 교체
    -->

    <nav>
        <a href="/about">소개</a>
        <!-- 일반 링크도 AJAX로 처리됨! -->
    </nav>

    <main>
        <!-- 콘텐츠 -->
    </main>
</body>


<!-- ================================================================== -->
<!-- 부스트 제외                                                         -->
<!-- ================================================================== -->

<a href="/external-site" hx-boost="false">
    외부 링크
</a>
<!-- 이 링크는 일반적으로 동작 (전체 페이지 이동) -->

<a href="/download.pdf" hx-boost="false" download>
    PDF 다운로드
</a>
<!-- 파일 다운로드도 부스트 제외 필요 -->
```

---

## 9. 디버깅

### 9.1 htmx.logAll()

```javascript
// 개발 중 모든 HTMX 이벤트 로깅
htmx.logAll();

// 출력 예:
// htmx:configRequest {elt: button, target: div#list, ...}
// htmx:beforeRequest {elt: button, xhr: XMLHttpRequest, ...}
// htmx:afterRequest {elt: button, successful: true, ...}
// htmx:beforeSwap {elt: button, serverResponse: "<div>...</div>", ...}
// htmx:afterSwap {elt: button, target: div#list, ...}
```

### 9.2 네트워크 탭

```
개발자 도구 > Network 탭에서 확인할 것:

1. 요청 헤더:
   HX-Request: true         ← HTMX 요청 표시
   HX-Target: #item-list    ← 타겟 요소
   HX-Trigger: button#add   ← 트리거 요소

2. 응답 헤더:
   HX-Trigger: showToast    ← 서버에서 발생시킨 이벤트
   HX-Redirect: /new-page   ← 리다이렉트 지시

3. 응답 본문:
   HTML 조각이 올바른지 확인
```

### 9.3 일반적인 문제

```html
<!-- 문제 1: 요소가 업데이트되지 않음 -->
<!-- 확인: hx-target이 올바른지? -->
<button hx-get="/data" hx-target="#wrong-id">로드</button>
<!-- #wrong-id가 실제로 존재하는가? -->


<!-- 문제 2: 이벤트가 발생하지 않음 -->
<!-- 확인: 이벤트 이름이 올바른지? -->
<div @showtoast.window="...">
<!-- showToast vs showtoast (대소문자 구분!) -->


<!-- 문제 3: hx-trigger가 작동하지 않음 -->
<!-- 확인: 이벤트 타입이 요소에 맞는지? -->
<input hx-trigger="click">  <!-- input에는 보통 change나 keyup 사용 -->


<!-- 문제 4: 중복 요청 -->
<!-- 확인: hx-trigger에 "once"를 추가하거나 hx-disabled-elt 사용 -->
<button hx-get="/data" hx-trigger="click once">로드</button>
```

---

## 10. 참고 자료

- [HTMX 공식 문서](https://htmx.org/docs/) - 가장 중요한 자료
- [HTMX 예제](https://htmx.org/examples/) - 실용적인 예제들
- [HTMX 속성 참조](https://htmx.org/reference/) - 모든 속성 목록
- [HTMX + FastAPI 예제](https://github.com/renceInbox/fastapi-todo) - 실전 예제

### 10.1 공부 순서 추천

1. hx-get, hx-post로 기본 요청 보내기
2. hx-target, hx-swap으로 응답 삽입 제어하기
3. hx-trigger로 다양한 이벤트 처리하기
4. 서버 응답 헤더 (HX-Trigger 등) 활용하기
5. Alpine.js와 함께 모달, 토스트 등 구현하기
6. hx-boost로 SPA 같은 네비게이션 구현하기
