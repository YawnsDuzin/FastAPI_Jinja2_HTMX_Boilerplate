# Alpine.js 가이드

## 1. Alpine.js 소개

Alpine.js는 가벼운 JavaScript 프레임워크로, HTML 속성만으로 동적인 상호작용을 구현할 수 있습니다. HTMX와 함께 사용하면 복잡한 클라이언트 사이드 로직도 간단하게 처리할 수 있습니다.

### 주요 특징
- **가벼움**: ~15KB (gzipped)
- **선언적**: HTML 속성으로 동작 정의
- **반응형**: 데이터 변경 시 자동 UI 업데이트
- **Vue.js 유사 문법**: 익숙한 구문

## 2. 기본 문법

### 2.1 x-data (상태 정의)

```html
<!-- 기본 상태 -->
<div x-data="{ open: false }">
    <button @click="open = !open">토글</button>
    <div x-show="open">내용</div>
</div>

<!-- 객체 상태 -->
<div x-data="{ user: { name: '', email: '' } }">
    <input x-model="user.name" placeholder="이름">
    <input x-model="user.email" placeholder="이메일">
    <p x-text="user.name"></p>
</div>

<!-- 메서드 포함 -->
<div x-data="{
    count: 0,
    increment() { this.count++ },
    decrement() { this.count-- }
}">
    <button @click="decrement">-</button>
    <span x-text="count"></span>
    <button @click="increment">+</button>
</div>
```

### 2.2 x-show / x-if (조건부 렌더링)

```html
<!-- x-show: CSS로 숨김/표시 -->
<div x-data="{ visible: true }">
    <div x-show="visible">보입니다</div>
</div>

<!-- x-show with transition -->
<div x-show="open"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0 scale-95"
     x-transition:enter-end="opacity-100 scale-100"
     x-transition:leave="transition ease-in duration-150"
     x-transition:leave-start="opacity-100 scale-100"
     x-transition:leave-end="opacity-0 scale-95">
    애니메이션과 함께
</div>

<!-- x-if: DOM에서 제거/추가 -->
<template x-if="condition">
    <div>조건이 참일 때만 DOM에 존재</div>
</template>
```

### 2.3 x-for (반복)

```html
<div x-data="{ items: ['사과', '바나나', '체리'] }">
    <template x-for="(item, index) in items" :key="index">
        <div>
            <span x-text="index + 1"></span>.
            <span x-text="item"></span>
        </div>
    </template>
</div>
```

### 2.4 x-model (양방향 바인딩)

```html
<div x-data="{ message: '' }">
    <!-- 텍스트 입력 -->
    <input type="text" x-model="message">
    <p x-text="message"></p>

    <!-- 체크박스 -->
    <input type="checkbox" x-model="agree">

    <!-- 라디오 -->
    <input type="radio" value="a" x-model="selected">
    <input type="radio" value="b" x-model="selected">

    <!-- 셀렉트 -->
    <select x-model="selected">
        <option value="a">A</option>
        <option value="b">B</option>
    </select>
</div>

<!-- 수식어 -->
<input x-model.lazy="name">      <!-- change 이벤트에서만 -->
<input x-model.number="age">     <!-- 숫자로 변환 -->
<input x-model.debounce="query"> <!-- 디바운스 -->
```

### 2.5 이벤트 핸들링

```html
<!-- @click -->
<button @click="open = true">열기</button>

<!-- @click.prevent -->
<form @submit.prevent="handleSubmit">

<!-- @click.stop -->
<button @click.stop="doSomething">이벤트 전파 중단</button>

<!-- @click.outside -->
<div x-data="{ open: false }">
    <button @click="open = true">열기</button>
    <div x-show="open" @click.outside="open = false">
        바깥 클릭 시 닫힘
    </div>
</div>

<!-- @keyup -->
<input @keyup.enter="submit">
<input @keyup.escape="cancel">

<!-- 디바운스 -->
<input @keyup.debounce.300ms="search">
```

### 2.6 x-text / x-html

```html
<!-- 텍스트 출력 -->
<span x-text="message"></span>

<!-- HTML 출력 (주의: XSS 위험) -->
<div x-html="htmlContent"></div>
```

### 2.7 x-bind (속성 바인딩)

```html
<!-- 클래스 바인딩 -->
<div :class="{ 'active': isActive, 'hidden': !visible }">

<!-- 스타일 바인딩 -->
<div :style="{ color: textColor, fontSize: fontSize + 'px' }">

<!-- 일반 속성 -->
<input :disabled="isDisabled">
<img :src="imageUrl">
<a :href="link">

<!-- 축약형 -->
<div :class="classes">  <!-- x-bind:class와 동일 -->
```

## 3. 고급 기능

### 3.1 x-init (초기화)

```html
<div x-data="{ items: [] }"
     x-init="items = await fetch('/api/items').then(r => r.json())">
    ...
</div>

<!-- 컴포넌트 초기화 -->
<div x-data="dropdown()"
     x-init="init()">
    ...
</div>
```

### 3.2 x-effect (반응형 효과)

```html
<div x-data="{ count: 0 }"
     x-effect="console.log('count changed to:', count)">
    <button @click="count++">증가</button>
</div>
```

### 3.3 $dispatch (이벤트 발송)

```html
<!-- 이벤트 발송 -->
<button @click="$dispatch('custom-event', { message: 'hello' })">
    이벤트 발송
</button>

<!-- 이벤트 수신 -->
<div @custom-event.window="handleEvent($event.detail)">
    ...
</div>

<!-- HTMX와 함께 사용 -->
<button @click="$dispatch('openModal')">모달 열기</button>
```

### 3.4 $refs (요소 참조)

```html
<div x-data>
    <input x-ref="input" type="text">
    <button @click="$refs.input.focus()">포커스</button>
</div>
```

### 3.5 $watch (변경 감지)

```html
<div x-data="{ count: 0 }"
     x-init="$watch('count', value => console.log(value))">
    <button @click="count++">증가</button>
</div>
```

## 4. 이 프로젝트의 Alpine.js 패턴

### 4.1 다크 모드 토글

```html
<html x-data="{ darkMode: localStorage.getItem('darkMode') === 'true' }"
      :class="{ 'dark': darkMode }">
    <body>
        <button @click="
            darkMode = !darkMode;
            localStorage.setItem('darkMode', darkMode)
        ">
            <span x-show="!darkMode">🌙</span>
            <span x-show="darkMode">☀️</span>
        </button>
    </body>
</html>
```

### 4.2 드롭다운 메뉴

```html
<div x-data="{ open: false }">
    <button @click="open = !open">메뉴</button>

    <div x-show="open"
         @click.outside="open = false"
         x-transition>
        <a href="/profile">프로필</a>
        <a href="/settings">설정</a>
    </div>
</div>
```

### 4.3 모달

```html
<div x-data="{ open: false }"
     @openModal.window="open = true"
     @closeModal.window="open = false"
     @keydown.escape.window="open = false">

    <!-- 배경 -->
    <div x-show="open"
         x-transition:enter="transition ease-out duration-200"
         x-transition:leave="transition ease-in duration-150"
         class="fixed inset-0 bg-black/50"
         @click="open = false">
    </div>

    <!-- 모달 내용 -->
    <div x-show="open"
         x-transition
         id="modal-content"
         class="fixed inset-0 flex items-center justify-center">
        <!-- HTMX가 여기에 내용 삽입 -->
    </div>
</div>
```

### 4.4 토스트 핸들러

```html
<div id="toast-container"
     x-data="toastHandler()"
     @showToast.window="show($event.detail)">
    <template x-for="toast in toasts" :key="toast.id">
        <div x-show="true"
             x-transition
             :class="{
                 'bg-green-500': toast.type === 'success',
                 'bg-red-500': toast.type === 'error',
                 'bg-blue-500': toast.type === 'info'
             }">
            <span x-text="toast.message"></span>
            <button @click="remove(toast.id)">×</button>
        </div>
    </template>
</div>

<script>
function toastHandler() {
    return {
        toasts: [],
        show(detail) {
            const toast = {
                id: Date.now(),
                ...detail
            };
            this.toasts.push(toast);
            setTimeout(() => this.remove(toast.id), 5000);
        },
        remove(id) {
            this.toasts = this.toasts.filter(t => t.id !== id);
        }
    };
}
</script>
```

### 4.5 폼 유효성 검사

```html
<form x-data="{
    email: '',
    password: '',
    errors: {},
    validate() {
        this.errors = {};
        if (!this.email) this.errors.email = '이메일을 입력하세요';
        if (!this.password) this.errors.password = '비밀번호를 입력하세요';
        return Object.keys(this.errors).length === 0;
    }
}" @submit.prevent="if(validate()) $el.submit()">

    <div>
        <input type="email" x-model="email">
        <span x-show="errors.email" x-text="errors.email" class="text-red-500"></span>
    </div>

    <div>
        <input type="password" x-model="password">
        <span x-show="errors.password" x-text="errors.password" class="text-red-500"></span>
    </div>

    <button type="submit">로그인</button>
</form>
```

## 5. HTMX + Alpine.js 통합

```html
<!-- HTMX 이벤트를 Alpine에서 처리 -->
<div x-data="{ loading: false }"
     @htmx:before-request="loading = true"
     @htmx:after-request="loading = false">

    <button hx-get="/api/data"
            :disabled="loading">
        <span x-show="!loading">데이터 로드</span>
        <span x-show="loading">로딩 중...</span>
    </button>
</div>

<!-- Alpine에서 HTMX 트리거 -->
<button @click="$dispatch('openModal'); htmx.ajax('GET', '/modal', '#modal-content')">
    모달 열기
</button>
```

## 6. 참고 자료

- [Alpine.js 공식 문서](https://alpinejs.dev)
- [Alpine.js 시작하기](https://alpinejs.dev/start-here)
- [Alpine.js 디렉티브](https://alpinejs.dev/directives/data)
