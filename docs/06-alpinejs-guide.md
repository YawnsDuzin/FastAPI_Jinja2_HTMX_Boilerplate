# Alpine.js 가이드

## 1. Alpine.js란?

### 1.1 Alpine.js 소개

Alpine.js는 HTML 안에서 직접 JavaScript 동작을 정의할 수 있는 **가벼운 JavaScript 프레임워크**입니다.

```
기존 JavaScript 방식:
HTML 파일 → JavaScript 파일 → DOM 조작 → 복잡한 연결

Alpine.js 방식:
HTML 파일 안에서 직접 동작 정의 → 간단!
```

### 1.2 왜 Alpine.js를 사용하나요?

Python 개발자 관점에서 설명하면:

```python
# Python에서 조건문
if is_visible:
    print("보입니다")
```

```html
<!-- Alpine.js에서 조건문 (HTML 안에서!) -->
<div x-show="isVisible">보입니다</div>
```

HTML 속성만으로 JavaScript 로직을 구현할 수 있습니다!

### 1.3 Alpine.js vs 다른 프레임워크

| 특징 | Alpine.js | React/Vue |
|------|-----------|-----------|
| 크기 | ~15KB | 100KB+ |
| 학습 곡선 | 낮음 | 높음 |
| 빌드 도구 | 불필요 | 필요 |
| 사용 방식 | HTML 속성 | 별도 컴포넌트 |

Alpine.js는 "작은 Vue.js"라고 불립니다. HTMX와 함께 사용하면 복잡한 프레임워크 없이도 동적인 웹 애플리케이션을 만들 수 있습니다.

---

## 2. Alpine.js 설치

### 2.1 CDN으로 설치

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <!-- 페이지 내용 -->

    <!-- Alpine.js CDN (body 끝에 배치) -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <!-- defer: HTML 파싱 완료 후 스크립트 실행 -->
    <!-- @3.x.x: 버전 3의 최신 버전 사용 -->
</body>
</html>
```

### 2.2 로컬 파일로 설치

```html
<!-- 다운로드한 파일 사용 -->
<script defer src="/static/js/alpine.min.js"></script>
```

---

## 3. x-data: 상태(데이터) 정의

### 3.1 기본 개념

`x-data`는 Alpine.js의 **가장 핵심적인 속성**입니다. Python의 클래스 인스턴스 변수와 비슷합니다.

```python
# Python 클래스
class Counter:
    def __init__(self):
        self.count = 0  # 상태 정의
```

```html
<!-- Alpine.js x-data -->
<div x-data="{ count: 0 }">
    <!-- x-data: Alpine.js 상태를 정의하는 속성 -->
    <!-- { count: 0 }: JavaScript 객체 형태로 상태 정의 -->
    <!-- count라는 변수에 초기값 0을 할당 -->

    <!-- 이 div 안에서 count 변수 사용 가능 -->
</div>
```

### 3.2 여러 상태 정의

```html
<div x-data="{
    count: 0,
    name: '홍길동',
    isActive: true,
    items: ['사과', '바나나']
}">
    <!-- count: 숫자 타입 -->
    <!-- name: 문자열 타입 -->
    <!-- isActive: 불리언(참/거짓) 타입 -->
    <!-- items: 배열 타입 -->
</div>
```

### 3.3 객체 상태

```html
<div x-data="{
    user: {
        name: '홍길동',
        email: 'hong@example.com',
        age: 25
    }
}">
    <!-- user: 중첩된 객체 -->
    <!-- Python의 딕셔너리와 비슷: {'name': '홍길동', ...} -->

    <!-- 접근 방법: user.name, user.email, user.age -->
</div>
```

### 3.4 메서드(함수) 포함

```html
<div x-data="{
    count: 0,

    increment() {
        this.count++
    },

    decrement() {
        this.count--
    },

    reset() {
        this.count = 0
    }
}">
    <!-- increment(): count를 1 증가시키는 메서드 -->
    <!-- this.count: 같은 x-data 내의 count 변수 참조 -->
    <!-- this: Python의 self와 같은 역할 -->
</div>
```

Python으로 비교하면:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def reset(self):
        self.count = 0
```

### 3.5 x-data 스코프(범위)

```html
<div x-data="{ message: '안녕하세요' }">
    <!-- 여기서 message 사용 가능 -->
    <p x-text="message"></p>

    <div>
        <!-- 자식 요소에서도 message 사용 가능 -->
        <span x-text="message"></span>
    </div>
</div>

<!-- 여기서는 message 사용 불가! (x-data 범위 밖) -->
<p x-text="message"></p>  <!-- 작동 안 함 -->
```

```
x-data 범위:
┌─────────────────────────────┐
│ <div x-data="{ msg: 'hi' }">│
│   ┌─────────────────────┐   │
│   │ msg 사용 가능 ✓     │   │
│   │   ┌─────────────┐   │   │
│   │   │ msg 가능 ✓  │   │   │
│   │   └─────────────┘   │   │
│   └─────────────────────┘   │
│ </div>                      │
└─────────────────────────────┘
  msg 사용 불가 ✗
```

---

## 4. x-text와 x-html: 텍스트 출력

### 4.1 x-text

`x-text`는 요소의 텍스트 내용을 JavaScript 표현식 결과로 설정합니다.

```html
<div x-data="{ name: '홍길동', count: 42 }">

    <!-- 기본 사용 -->
    <p x-text="name"></p>
    <!-- 결과: <p>홍길동</p> -->
    <!-- x-text="name": name 변수의 값을 텍스트로 표시 -->

    <!-- 문자열 연결 -->
    <p x-text="'안녕하세요, ' + name + '님!'"></p>
    <!-- 결과: <p>안녕하세요, 홍길동님!</p> -->
    <!-- JavaScript 문자열 연결 사용 -->

    <!-- 템플릿 리터럴 (백틱 사용) -->
    <p x-text="`환영합니다, ${name}님!`"></p>
    <!-- 결과: <p>환영합니다, 홍길동님!</p> -->
    <!-- ${변수}: 변수 값 삽입 (Python의 f-string과 유사) -->

    <!-- 계산 표현식 -->
    <p x-text="count * 2"></p>
    <!-- 결과: <p>84</p> -->
    <!-- 수학 연산도 가능 -->

    <!-- 조건 표현식 (삼항 연산자) -->
    <p x-text="count > 40 ? '많음' : '적음'"></p>
    <!-- 결과: <p>많음</p> -->
    <!-- 조건 ? 참일때 : 거짓일때 -->
    <!-- Python: '많음' if count > 40 else '적음' -->

</div>
```

### 4.2 x-html (주의 필요!)

`x-html`은 HTML 태그를 포함한 내용을 렌더링합니다.

```html
<div x-data="{
    htmlContent: '<strong>굵은 글씨</strong>',
    userInput: '<script>alert(\"해킹!\")</script>'
}">

    <!-- HTML 렌더링 -->
    <div x-html="htmlContent"></div>
    <!-- 결과: <div><strong>굵은 글씨</strong></div> -->
    <!-- strong 태그가 실제로 적용됨 -->

    <!-- ⚠️ 위험! 사용자 입력에는 절대 사용 금지 -->
    <div x-html="userInput"></div>
    <!-- XSS(크로스 사이트 스크립팅) 공격 위험! -->

</div>
```

**보안 규칙:**
- `x-html`은 **신뢰할 수 있는 데이터**에만 사용
- 사용자가 입력한 데이터는 반드시 `x-text` 사용
- 서버에서 받은 데이터도 검증 필요

---

## 5. x-show와 x-if: 조건부 표시

### 5.1 x-show

`x-show`는 CSS `display` 속성으로 요소를 숨기거나 표시합니다.

```html
<div x-data="{ isVisible: true }">

    <!-- 기본 사용 -->
    <p x-show="isVisible">이 텍스트가 보입니다</p>
    <!-- isVisible이 true면 표시, false면 숨김 -->
    <!-- 숨길 때: style="display: none;" 자동 추가 -->

    <!-- 변수 기반 조건 -->
    <p x-show="!isVisible">isVisible이 false일 때 보임</p>
    <!-- !isVisible: isVisible의 반대 (not 연산) -->

    <!-- 비교 연산 -->
    <div x-data="{ count: 5 }">
        <p x-show="count > 0">양수입니다</p>
        <p x-show="count === 0">0입니다</p>
        <p x-show="count < 0">음수입니다</p>
        <!-- ===: JavaScript의 일치 연산자 (Python의 ==) -->
    </div>

</div>
```

**x-show의 특징:**
```
x-show="false"일 때:
- DOM에 요소가 존재함 (HTML에 있음)
- CSS로 숨김 (display: none)
- 빠른 토글에 적합
```

### 5.2 x-if

`x-if`는 조건에 따라 DOM에서 요소를 추가/제거합니다.

```html
<div x-data="{ showDetails: false }">

    <!-- template 태그 필수! -->
    <template x-if="showDetails">
        <div class="details">
            <h3>상세 정보</h3>
            <p>이 내용은 showDetails가 true일 때만 DOM에 존재합니다.</p>
        </div>
    </template>
    <!-- template: 브라우저가 렌더링하지 않는 특수 태그 -->
    <!-- x-if는 반드시 template 태그와 함께 사용 -->

</div>
```

**x-if의 특징:**
```
x-if="false"일 때:
- DOM에서 요소가 완전히 제거됨
- 다시 true가 되면 새로 생성
- 무거운 컴포넌트에 적합
```

### 5.3 x-show vs x-if 비교

```html
<div x-data="{ show: true }">

    <!-- x-show: 자주 토글할 때 -->
    <div x-show="show">x-show로 숨김/표시</div>
    <!-- 장점: 빠른 토글 -->
    <!-- 단점: 숨겨도 DOM에 존재 -->

    <!-- x-if: 조건이 잘 바뀌지 않을 때 -->
    <template x-if="show">
        <div>x-if로 추가/제거</div>
    </template>
    <!-- 장점: false일 때 DOM에서 완전 제거 -->
    <!-- 단점: 토글 시 DOM 재생성 비용 -->

</div>
```

| 상황 | 추천 |
|------|------|
| 드롭다운 메뉴, 툴팁 | x-show |
| 탭 패널 (자주 전환) | x-show |
| 로그인 후에만 표시 | x-if |
| 조건부 폼 필드 | x-if |

---

## 6. x-bind: 속성 바인딩

### 6.1 기본 사용법

`x-bind`는 HTML 속성을 JavaScript 표현식과 연결합니다.

```html
<div x-data="{
    imageUrl: '/static/images/photo.jpg',
    linkUrl: 'https://example.com',
    isDisabled: true,
    buttonText: '클릭하세요'
}">

    <!-- 이미지 src 바인딩 -->
    <img x-bind:src="imageUrl" alt="사진">
    <!-- x-bind:src: src 속성을 imageUrl 변수와 연결 -->
    <!-- 결과: <img src="/static/images/photo.jpg" alt="사진"> -->

    <!-- 링크 href 바인딩 -->
    <a x-bind:href="linkUrl">링크</a>
    <!-- 결과: <a href="https://example.com">링크</a> -->

    <!-- disabled 속성 바인딩 -->
    <button x-bind:disabled="isDisabled">버튼</button>
    <!-- isDisabled가 true면: <button disabled>버튼</button> -->
    <!-- isDisabled가 false면: <button>버튼</button> -->

    <!-- 여러 속성 동시 바인딩 -->
    <input
        x-bind:placeholder="buttonText"
        x-bind:disabled="isDisabled"
        x-bind:value="buttonText">

</div>
```

### 6.2 축약 문법 (`:` 사용)

```html
<div x-data="{ url: '/page', active: true }">

    <!-- x-bind:href 대신 :href 사용 -->
    <a :href="url">링크</a>

    <!-- x-bind:disabled 대신 :disabled -->
    <button :disabled="!active">버튼</button>

    <!-- 훨씬 간결! 실제 코드에서는 축약형 권장 -->

</div>
```

### 6.3 클래스 바인딩

```html
<div x-data="{ isActive: true, hasError: false, isLarge: true }">

    <!-- 객체 문법: 조건에 따라 클래스 추가/제거 -->
    <div :class="{ 'active': isActive, 'error': hasError }">
        내용
    </div>
    <!-- 결과: <div class="active">내용</div> -->
    <!-- isActive가 true이므로 'active' 클래스 추가 -->
    <!-- hasError가 false이므로 'error' 클래스 미추가 -->

    <!-- 기존 클래스와 함께 사용 -->
    <div class="card" :class="{ 'card-active': isActive }">
        카드
    </div>
    <!-- 결과: <div class="card card-active">카드</div> -->
    <!-- 기존 'card' 클래스 유지 + 조건부 클래스 추가 -->

    <!-- 여러 조건 -->
    <button :class="{
        'btn-primary': isActive,
        'btn-danger': hasError,
        'btn-lg': isLarge
    }">버튼</button>
    <!-- 결과: <button class="btn-primary btn-lg">버튼</button> -->

    <!-- 배열 문법 -->
    <div :class="[isActive ? 'active' : 'inactive', 'base-class']">
        내용
    </div>
    <!-- 삼항 연산자 + 배열로 복잡한 로직 가능 -->

</div>
```

### 6.4 스타일 바인딩

```html
<div x-data="{
    textColor: 'red',
    fontSize: 20,
    isVisible: true
}">

    <!-- 객체 문법 -->
    <p :style="{ color: textColor, fontSize: fontSize + 'px' }">
        스타일 적용된 텍스트
    </p>
    <!-- 결과: <p style="color: red; font-size: 20px;">...</p> -->
    <!-- fontSize + 'px': 숫자에 단위 추가 -->

    <!-- 조건부 스타일 -->
    <div :style="{ display: isVisible ? 'block' : 'none' }">
        조건부 표시
    </div>

    <!-- camelCase 사용 (JavaScript 규칙) -->
    <div :style="{
        backgroundColor: 'blue',
        marginTop: '10px',
        borderRadius: '5px'
    }">
        <!-- CSS: background-color → JS: backgroundColor -->
        <!-- CSS: margin-top → JS: marginTop -->
    </div>

</div>
```

---

## 7. @click과 이벤트 핸들링

### 7.1 @click 기본

`@click`은 클릭 이벤트를 처리합니다. `x-on:click`의 축약형입니다.

```html
<div x-data="{ count: 0, message: '' }">

    <!-- 기본 클릭 -->
    <button @click="count++">
        클릭 횟수: <span x-text="count"></span>
    </button>
    <!-- @click="count++": 클릭하면 count를 1 증가 -->

    <!-- 값 변경 -->
    <button @click="message = '안녕하세요!'">
        인사하기
    </button>
    <!-- 클릭하면 message 변수에 문자열 할당 -->

    <!-- 여러 동작 (세미콜론으로 구분) -->
    <button @click="count++; message = '증가!'">
        증가 + 메시지
    </button>

    <!-- 메서드 호출 -->
    <button @click="increment()">증가</button>
    <!-- x-data에 정의된 메서드 호출 -->

</div>
```

### 7.2 다른 이벤트들

```html
<div x-data="{ value: '', focused: false }">

    <!-- 입력 이벤트 -->
    <input
        @input="value = $event.target.value"
        @focus="focused = true"
        @blur="focused = false">
    <!-- @input: 입력할 때마다 발생 -->
    <!-- @focus: 포커스 받을 때 -->
    <!-- @blur: 포커스 잃을 때 -->
    <!-- $event: 이벤트 객체 -->
    <!-- $event.target: 이벤트가 발생한 요소 -->

    <!-- 키보드 이벤트 -->
    <input
        @keyup="handleKey()"
        @keydown.enter="submit()"
        @keyup.escape="cancel()">
    <!-- @keyup: 키를 뗄 때 -->
    <!-- @keydown: 키를 누를 때 -->
    <!-- .enter: Enter 키만 감지 -->
    <!-- .escape: Escape 키만 감지 -->

    <!-- 마우스 이벤트 -->
    <div
        @mouseenter="hovered = true"
        @mouseleave="hovered = false">
        마우스 올려보세요
    </div>
    <!-- @mouseenter: 마우스가 들어올 때 -->
    <!-- @mouseleave: 마우스가 나갈 때 -->

    <!-- 폼 이벤트 -->
    <form @submit.prevent="handleSubmit()">
        <button type="submit">제출</button>
    </form>
    <!-- @submit: 폼 제출 시 -->
    <!-- .prevent: 기본 동작 방지 (페이지 새로고침 방지) -->

</div>
```

### 7.3 이벤트 수식어 (Modifiers)

```html
<div x-data="{ }">

    <!-- .prevent: 기본 동작 방지 -->
    <a href="/page" @click.prevent="customAction()">
        링크
    </a>
    <!-- 클릭해도 페이지 이동 안 함 -->
    <!-- Python에서 event.preventDefault()와 같음 -->

    <!-- .stop: 이벤트 버블링 중지 -->
    <div @click="parentClick()">
        <button @click.stop="childClick()">
            버튼
        </button>
    </div>
    <!-- 버튼 클릭 시 parentClick은 실행 안 됨 -->

    <!-- .outside: 요소 바깥 클릭 감지 -->
    <div x-data="{ open: false }">
        <button @click="open = true">열기</button>
        <div x-show="open" @click.outside="open = false">
            드롭다운 내용
            <!-- 이 div 바깥을 클릭하면 닫힘 -->
        </div>
    </div>

    <!-- .once: 한 번만 실행 -->
    <button @click.once="initialize()">
        초기화 (한 번만)
    </button>

    <!-- .self: 자기 자신 클릭 시에만 -->
    <div @click.self="onlyDiv()">
        <button>이 버튼 클릭은 무시</button>
        <!-- div 자체를 클릭해야 실행 -->
    </div>

    <!-- .window: window 객체에 이벤트 연결 -->
    <div @keydown.escape.window="closeModal()">
        <!-- 페이지 어디서든 Escape 누르면 실행 -->
    </div>

    <!-- 키보드 수식어 -->
    <input
        @keydown.enter="submit()"
        @keydown.arrow-up="moveUp()"
        @keydown.arrow-down="moveDown()"
        @keydown.ctrl.s="save()">
    <!-- .ctrl, .shift, .alt: 조합 키 -->

    <!-- .debounce: 연속 이벤트 제어 -->
    <input @input.debounce.300ms="search()">
    <!-- 입력 후 300ms 기다린 후 실행 -->
    <!-- 빠른 타이핑 시 마지막 입력만 처리 -->

</div>
```

---

## 8. x-model: 양방향 데이터 바인딩

### 8.1 기본 개념

`x-model`은 폼 입력과 데이터를 **양방향으로 연결**합니다.

```
양방향 바인딩:
데이터 → 입력 필드 (데이터 변경 시 입력 필드 업데이트)
입력 필드 → 데이터 (사용자 입력 시 데이터 업데이트)
```

```html
<div x-data="{ name: '홍길동' }">

    <!-- 입력 필드 -->
    <input type="text" x-model="name">
    <!-- 초기값: name 변수의 값 '홍길동'이 표시됨 -->
    <!-- 사용자가 입력하면: name 변수가 자동 업데이트 -->

    <!-- 실시간 반영 확인 -->
    <p>입력한 이름: <span x-text="name"></span></p>
    <!-- name이 변경되면 자동으로 업데이트 -->

</div>
```

### 8.2 다양한 입력 타입

```html
<div x-data="{
    text: '',
    number: 0,
    checked: false,
    selected: 'a',
    multiple: [],
    textarea: ''
}">

    <!-- 텍스트 입력 -->
    <input type="text" x-model="text" placeholder="텍스트 입력">

    <!-- 숫자 입력 -->
    <input type="number" x-model="number">
    <!-- 주의: 기본적으로 문자열로 저장됨 -->

    <!-- 체크박스 (단일) -->
    <label>
        <input type="checkbox" x-model="checked">
        동의합니다
    </label>
    <!-- checked: true 또는 false -->

    <!-- 체크박스 (다중) -->
    <label>
        <input type="checkbox" value="option1" x-model="multiple">
        옵션 1
    </label>
    <label>
        <input type="checkbox" value="option2" x-model="multiple">
        옵션 2
    </label>
    <!-- multiple: ['option1', 'option2'] 형태의 배열 -->

    <!-- 라디오 버튼 -->
    <label>
        <input type="radio" value="a" x-model="selected">
        A 선택
    </label>
    <label>
        <input type="radio" value="b" x-model="selected">
        B 선택
    </label>
    <!-- selected: 선택된 값 ('a' 또는 'b') -->

    <!-- 셀렉트 박스 -->
    <select x-model="selected">
        <option value="a">옵션 A</option>
        <option value="b">옵션 B</option>
        <option value="c">옵션 C</option>
    </select>

    <!-- 텍스트 영역 -->
    <textarea x-model="textarea" rows="4"></textarea>

</div>
```

### 8.3 x-model 수식어

```html
<div x-data="{
    lazyValue: '',
    numberValue: 0,
    debouncedValue: ''
}">

    <!-- .lazy: change 이벤트에서만 업데이트 -->
    <input type="text" x-model.lazy="lazyValue">
    <!-- 입력 중에는 업데이트 안 함 -->
    <!-- 포커스를 벗어나면 (blur) 업데이트 -->
    <!-- 성능 최적화에 유용 -->

    <!-- .number: 숫자로 자동 변환 -->
    <input type="number" x-model.number="numberValue">
    <!-- 입력값을 자동으로 숫자 타입으로 변환 -->
    <!-- "123" → 123 -->

    <!-- .debounce: 디바운스 적용 -->
    <input type="text" x-model.debounce="debouncedValue">
    <!-- 입력 후 일정 시간 기다린 후 업데이트 -->
    <!-- 기본값: 250ms -->

    <!-- .debounce.500ms: 시간 지정 -->
    <input type="text" x-model.debounce.500ms="debouncedValue">
    <!-- 500ms 대기 후 업데이트 -->

    <!-- .trim: 앞뒤 공백 제거 -->
    <input type="text" x-model.trim="text">
    <!-- "  hello  " → "hello" -->

</div>
```

---

## 9. x-for: 반복 렌더링

### 9.1 기본 사용법

`x-for`는 배열의 각 항목을 반복하여 렌더링합니다.

```html
<div x-data="{ items: ['사과', '바나나', '체리'] }">

    <!-- 기본 반복 -->
    <template x-for="item in items">
        <div x-text="item"></div>
    </template>
    <!-- 결과: -->
    <!-- <div>사과</div> -->
    <!-- <div>바나나</div> -->
    <!-- <div>체리</div> -->

    <!-- x-for는 반드시 template 태그와 함께! -->
    <!-- template 안에는 하나의 루트 요소만! -->

</div>
```

Python과 비교:
```python
items = ['사과', '바나나', '체리']
for item in items:
    print(item)
```

### 9.2 인덱스 사용

```html
<div x-data="{ items: ['사과', '바나나', '체리'] }">

    <!-- 인덱스와 함께 -->
    <template x-for="(item, index) in items">
        <div>
            <span x-text="index + 1"></span>.
            <span x-text="item"></span>
        </div>
    </template>
    <!-- 결과: -->
    <!-- <div>1. 사과</div> -->
    <!-- <div>2. 바나나</div> -->
    <!-- <div>3. 체리</div> -->

    <!-- index: 0부터 시작하는 인덱스 -->
    <!-- index + 1: 1부터 시작하도록 -->

</div>
```

### 9.3 :key 속성

```html
<div x-data="{
    users: [
        { id: 1, name: '홍길동' },
        { id: 2, name: '김철수' },
        { id: 3, name: '이영희' }
    ]
}">

    <!-- :key로 고유 식별자 지정 -->
    <template x-for="user in users" :key="user.id">
        <div>
            <span x-text="user.name"></span>
        </div>
    </template>
    <!-- :key="user.id": 각 항목의 고유 식별자 -->
    <!-- Alpine이 효율적으로 DOM을 업데이트하는 데 사용 -->
    <!-- 항목 추가/삭제/재정렬 시 성능 향상 -->

</div>
```

**:key를 사용해야 하는 이유:**
```
key 없이:
- 배열 변경 시 모든 요소 다시 렌더링
- 비효율적

key 있으면:
- 변경된 부분만 업데이트
- 효율적인 DOM 조작
```

### 9.4 객체 배열 반복

```html
<div x-data="{
    products: [
        { id: 1, name: '노트북', price: 1200000 },
        { id: 2, name: '마우스', price: 50000 },
        { id: 3, name: '키보드', price: 100000 }
    ]
}">

    <table>
        <thead>
            <tr>
                <th>번호</th>
                <th>상품명</th>
                <th>가격</th>
            </tr>
        </thead>
        <tbody>
            <template x-for="(product, index) in products" :key="product.id">
                <tr>
                    <td x-text="index + 1"></td>
                    <td x-text="product.name"></td>
                    <td x-text="product.price.toLocaleString() + '원'"></td>
                    <!-- toLocaleString(): 1200000 → "1,200,000" -->
                </tr>
            </template>
        </tbody>
    </table>

</div>
```

### 9.5 숫자 범위 반복

```html
<div x-data="{ total: 5 }">

    <!-- 숫자 범위 반복 -->
    <template x-for="n in 5">
        <span x-text="n"></span>
        <!-- 결과: 1 2 3 4 5 -->
    </template>

    <!-- 변수 사용 -->
    <template x-for="n in total">
        <span x-text="n"></span>
    </template>

    <!-- 별점 표시 예시 -->
    <div x-data="{ rating: 3 }">
        <template x-for="n in 5">
            <span :class="{ 'text-yellow-500': n <= rating }">★</span>
        </template>
        <!-- 결과: ★★★☆☆ (3개 노란색) -->
    </div>

</div>
```

---

## 10. x-transition: 애니메이션

### 10.1 기본 트랜지션

`x-transition`은 요소가 나타나거나 사라질 때 애니메이션을 적용합니다.

```html
<div x-data="{ open: false }">
    <button @click="open = !open">토글</button>

    <!-- 기본 트랜지션 (페이드 + 스케일) -->
    <div x-show="open" x-transition>
        애니메이션과 함께 나타남/사라짐
    </div>
    <!-- 기본 효과: 투명도 + 크기 변화 -->

</div>
```

### 10.2 트랜지션 커스터마이징

```html
<div x-data="{ open: false }">
    <button @click="open = !open">토글</button>

    <!-- 세밀한 제어 -->
    <div
        x-show="open"
        x-transition:enter="transition ease-out duration-300"
        x-transition:enter-start="opacity-0 transform scale-90"
        x-transition:enter-end="opacity-100 transform scale-100"
        x-transition:leave="transition ease-in duration-200"
        x-transition:leave-start="opacity-100 transform scale-100"
        x-transition:leave-end="opacity-0 transform scale-90"
    >
        커스텀 애니메이션
    </div>

    <!--
    x-transition:enter: 나타날 때 적용할 CSS 클래스
    x-transition:enter-start: 나타나기 시작할 때 상태
    x-transition:enter-end: 나타나기 끝날 때 상태

    x-transition:leave: 사라질 때 적용할 CSS 클래스
    x-transition:leave-start: 사라지기 시작할 때 상태
    x-transition:leave-end: 사라지기 끝날 때 상태

    Tailwind CSS 클래스 사용:
    - transition: CSS 트랜지션 활성화
    - ease-out/ease-in: 가속/감속 효과
    - duration-300: 300ms 지속
    - opacity-0/100: 투명도 0/100%
    - scale-90/100: 크기 90/100%
    -->

</div>
```

### 10.3 트랜지션 수식어

```html
<div x-data="{ open: false }">

    <!-- 지속 시간 설정 -->
    <div x-show="open" x-transition.duration.500ms>
        500ms 애니메이션
    </div>

    <!-- 나타날 때와 사라질 때 다른 시간 -->
    <div
        x-show="open"
        x-transition:enter.duration.500ms
        x-transition:leave.duration.200ms>
        나타날 때 느리게, 사라질 때 빠르게
    </div>

    <!-- 투명도만 (스케일 없이) -->
    <div x-show="open" x-transition.opacity>
        페이드만 적용
    </div>

    <!-- 스케일만 (투명도 없이) -->
    <div x-show="open" x-transition.scale>
        스케일만 적용
    </div>

    <!-- 스케일 시작점 설정 -->
    <div x-show="open" x-transition.scale.75>
        75%에서 시작하는 스케일
    </div>

    <!-- 원점 설정 -->
    <div x-show="open" x-transition.scale.origin.top>
        위에서부터 스케일
    </div>

</div>
```

### 10.4 슬라이드 애니메이션 예시

```html
<div x-data="{ open: false }" class="relative">
    <button @click="open = !open">메뉴 열기</button>

    <!-- 위에서 아래로 슬라이드 -->
    <div
        x-show="open"
        x-transition:enter="transition ease-out duration-200"
        x-transition:enter-start="opacity-0 -translate-y-2"
        x-transition:enter-end="opacity-100 translate-y-0"
        x-transition:leave="transition ease-in duration-150"
        x-transition:leave-start="opacity-100 translate-y-0"
        x-transition:leave-end="opacity-0 -translate-y-2"
        class="absolute top-full left-0 bg-white shadow-lg"
    >
        <a href="#">메뉴 1</a>
        <a href="#">메뉴 2</a>
        <a href="#">메뉴 3</a>
    </div>

    <!--
    -translate-y-2: 위로 약간 이동
    translate-y-0: 원래 위치
    결과: 위에서 아래로 미끄러지며 나타남
    -->

</div>
```

---

## 11. x-init과 x-effect: 초기화와 반응

### 11.1 x-init: 초기화

`x-init`은 컴포넌트가 초기화될 때 실행되는 코드를 정의합니다.

```html
<div x-data="{ message: '' }" x-init="message = '초기화됨!'">
    <p x-text="message"></p>
    <!-- 페이지 로드 시 '초기화됨!' 표시 -->
</div>

<!-- 비동기 초기화 -->
<div
    x-data="{ users: [] }"
    x-init="users = await (await fetch('/api/users')).json()"
>
    <!-- x-init: 컴포넌트 생성 시 실행 -->
    <!-- await fetch(): API에서 데이터 가져오기 -->
    <!-- .json(): JSON으로 파싱 -->

    <template x-for="user in users" :key="user.id">
        <div x-text="user.name"></div>
    </template>
</div>

<!-- 초기화 함수 분리 -->
<div
    x-data="{
        items: [],
        loading: true,

        async init() {
            try {
                const response = await fetch('/api/items');
                this.items = await response.json();
            } catch (error) {
                console.error('로드 실패:', error);
            } finally {
                this.loading = false;
            }
        }
    }"
    x-init="init()"
>
    <div x-show="loading">로딩 중...</div>
    <div x-show="!loading">
        <template x-for="item in items">
            <div x-text="item.name"></div>
        </template>
    </div>
</div>
```

### 11.2 x-effect: 반응형 효과

`x-effect`는 참조하는 데이터가 변경될 때마다 자동으로 실행됩니다.

```html
<div
    x-data="{ count: 0 }"
    x-effect="console.log('count 변경:', count)"
>
    <button @click="count++">증가</button>
    <p x-text="count"></p>

    <!-- x-effect: count가 변경될 때마다 console.log 실행 -->
    <!-- 초기 로드 시에도 한 번 실행 -->
</div>

<!-- 실용적인 예: localStorage 동기화 -->
<div
    x-data="{ theme: localStorage.getItem('theme') || 'light' }"
    x-effect="localStorage.setItem('theme', theme)"
>
    <!-- theme이 변경될 때마다 localStorage에 저장 -->

    <select x-model="theme">
        <option value="light">라이트 모드</option>
        <option value="dark">다크 모드</option>
    </select>
</div>

<!-- 문서 제목 업데이트 -->
<div
    x-data="{ pageTitle: '홈' }"
    x-effect="document.title = pageTitle + ' | 내 사이트'"
>
    <!-- pageTitle이 변경되면 브라우저 탭 제목 업데이트 -->

    <button @click="pageTitle = '설정'">설정 페이지로</button>
</div>
```

---

## 12. 매직 프로퍼티 ($로 시작하는 것들)

### 12.1 $el: 현재 요소

```html
<div x-data>
    <button @click="$el.style.backgroundColor = 'red'">
        나를 빨갛게!
    </button>
    <!-- $el: 이 버튼 요소 자체를 가리킴 -->

    <input
        x-data
        @focus="$el.select()"
        value="클릭하면 전체 선택"
    >
    <!-- 포커스 시 입력 내용 전체 선택 -->
</div>
```

### 12.2 $refs: 요소 참조

```html
<div x-data="{ }">
    <!-- x-ref로 요소에 이름 붙이기 -->
    <input x-ref="nameInput" type="text" placeholder="이름">
    <input x-ref="emailInput" type="email" placeholder="이메일">

    <!-- $refs로 참조하기 -->
    <button @click="$refs.nameInput.focus()">
        이름 입력란으로 포커스
    </button>
    <!-- $refs.nameInput: x-ref="nameInput"인 요소 -->
    <!-- .focus(): 해당 요소에 포커스 -->

    <button @click="alert($refs.emailInput.value)">
        이메일 값 확인
    </button>
    <!-- .value: input의 현재 값 -->
</div>
```

### 12.3 $dispatch: 커스텀 이벤트 발송

```html
<!-- 이벤트 발송 -->
<div x-data>
    <button @click="$dispatch('show-notification', { message: '안녕하세요!' })">
        알림 보내기
    </button>
    <!-- $dispatch('이벤트명', 데이터) -->
    <!-- 커스텀 이벤트를 발생시킴 -->
</div>

<!-- 이벤트 수신 (같은 페이지 어디서든) -->
<div
    x-data="{ notification: '' }"
    @show-notification.window="notification = $event.detail.message"
>
    <!-- @show-notification.window: window에서 이벤트 수신 -->
    <!-- $event.detail: $dispatch에서 전달한 데이터 -->

    <div x-show="notification" x-text="notification"></div>
</div>
```

### 12.4 $watch: 변경 감지

```html
<div
    x-data="{
        query: '',
        results: []
    }"
    x-init="$watch('query', value => {
        console.log('검색어 변경:', value);
        // API 호출 등
    })"
>
    <!-- $watch('변수명', 콜백함수) -->
    <!-- 변수가 변경될 때마다 콜백 실행 -->

    <input x-model="query" placeholder="검색어 입력">
</div>

<!-- 이전 값과 비교 -->
<div
    x-data="{ count: 0 }"
    x-init="$watch('count', (newValue, oldValue) => {
        console.log(`${oldValue}에서 ${newValue}로 변경`);
    })"
>
    <button @click="count++">증가</button>
</div>
```

### 12.5 $nextTick: DOM 업데이트 후 실행

```html
<div x-data="{ open: false }">
    <button @click="
        open = true;
        $nextTick(() => {
            $refs.input.focus();
        });
    ">
        열고 포커스
    </button>
    <!-- $nextTick: DOM이 업데이트된 후 실행 -->
    <!-- open = true로 요소가 나타난 후에 포커스 가능 -->

    <div x-show="open">
        <input x-ref="input" type="text">
    </div>
</div>
```

### 12.6 $event: 이벤트 객체

```html
<div x-data>
    <!-- 키 이벤트 -->
    <input @keyup="console.log('누른 키:', $event.key)">
    <!-- $event: 원본 DOM 이벤트 객체 -->
    <!-- $event.key: 누른 키의 이름 -->

    <!-- 마우스 위치 -->
    <div @mousemove="console.log($event.clientX, $event.clientY)">
        마우스를 움직여보세요
    </div>

    <!-- 폼 데이터 -->
    <form @submit.prevent="handleSubmit($event.target)">
        <input name="email" type="email">
        <button type="submit">제출</button>
    </form>
    <!-- $event.target: 이벤트가 발생한 요소 (form) -->
</div>
```

---

## 13. 컴포넌트 패턴

### 13.1 재사용 가능한 컴포넌트

```html
<!-- JavaScript로 컴포넌트 정의 -->
<script>
// 드롭다운 컴포넌트
function dropdown() {
    return {
        open: false,

        toggle() {
            this.open = !this.open;
        },

        close() {
            this.open = false;
        }
    };
}

// 카운터 컴포넌트
function counter(initialValue = 0) {
    return {
        count: initialValue,

        increment() {
            this.count++;
        },

        decrement() {
            if (this.count > 0) {
                this.count--;
            }
        },

        reset() {
            this.count = 0;
        }
    };
}
</script>

<!-- 컴포넌트 사용 -->
<div x-data="dropdown()">
    <button @click="toggle()">메뉴</button>
    <div x-show="open" @click.outside="close()">
        <a href="#">옵션 1</a>
        <a href="#">옵션 2</a>
    </div>
</div>

<!-- 매개변수와 함께 사용 -->
<div x-data="counter(10)">
    <button @click="decrement()">-</button>
    <span x-text="count"></span>
    <button @click="increment()">+</button>
</div>
```

### 13.2 전역 데이터 (Alpine.store)

```html
<script>
// 전역 스토어 정의
document.addEventListener('alpine:init', () => {
    Alpine.store('user', {
        name: '',
        email: '',
        isLoggedIn: false,

        login(name, email) {
            this.name = name;
            this.email = email;
            this.isLoggedIn = true;
        },

        logout() {
            this.name = '';
            this.email = '';
            this.isLoggedIn = false;
        }
    });

    Alpine.store('notifications', {
        items: [],

        add(message, type = 'info') {
            this.items.push({ id: Date.now(), message, type });
        },

        remove(id) {
            this.items = this.items.filter(item => item.id !== id);
        }
    });
});
</script>

<!-- 스토어 사용 -->
<div x-data>
    <!-- $store로 전역 스토어 접근 -->
    <div x-show="$store.user.isLoggedIn">
        <span x-text="$store.user.name"></span>님 환영합니다!
        <button @click="$store.user.logout()">로그아웃</button>
    </div>

    <div x-show="!$store.user.isLoggedIn">
        <button @click="$store.user.login('홍길동', 'hong@example.com')">
            로그인
        </button>
    </div>
</div>

<!-- 알림 표시 -->
<div x-data>
    <template x-for="notification in $store.notifications.items" :key="notification.id">
        <div :class="'alert-' + notification.type">
            <span x-text="notification.message"></span>
            <button @click="$store.notifications.remove(notification.id)">×</button>
        </div>
    </template>
</div>
```

---

## 14. HTMX와 Alpine.js 통합

### 14.1 HTMX 이벤트 처리

```html
<div
    x-data="{ loading: false, error: null }"
    @htmx:before-request="loading = true; error = null"
    @htmx:after-request="loading = false"
    @htmx:response-error="error = '요청 실패'"
>
    <!--
    HTMX 이벤트를 Alpine.js에서 처리:
    @htmx:before-request: HTMX 요청 시작 전
    @htmx:after-request: HTMX 요청 완료 후
    @htmx:response-error: 서버 에러 발생 시
    -->

    <!-- 로딩 표시 -->
    <div x-show="loading" class="spinner">로딩 중...</div>

    <!-- 에러 표시 -->
    <div x-show="error" x-text="error" class="error"></div>

    <!-- HTMX 버튼 -->
    <button
        hx-get="/api/data"
        hx-target="#result"
        :disabled="loading"
    >
        <span x-show="!loading">데이터 로드</span>
        <span x-show="loading">로딩...</span>
    </button>

    <div id="result"></div>
</div>
```

### 14.2 모달 통합

```html
<!-- 모달 컨테이너 -->
<div
    x-data="{ open: false }"
    @open-modal.window="open = true"
    @close-modal.window="open = false"
    @keydown.escape.window="open = false"
>
    <!-- 배경 오버레이 -->
    <div
        x-show="open"
        x-transition.opacity
        class="fixed inset-0 bg-black/50 z-40"
        @click="open = false"
    ></div>

    <!-- 모달 내용 -->
    <div
        x-show="open"
        x-transition
        class="fixed inset-0 flex items-center justify-center z-50"
    >
        <div
            id="modal-content"
            class="bg-white rounded-lg p-6 max-w-md"
            @click.stop
        >
            <!-- HTMX가 여기에 내용 삽입 -->
        </div>
    </div>
</div>

<!-- 모달 열기 버튼 -->
<button
    hx-get="/partials/modal/edit/1"
    hx-target="#modal-content"
    @htmx:after-request="$dispatch('open-modal')"
>
    편집
</button>
```

### 14.3 토스트 알림 시스템

```html
<!-- 토스트 컨테이너 -->
<div
    id="toast-container"
    x-data="toastHandler()"
    @show-toast.window="addToast($event.detail)"
    class="fixed bottom-4 right-4 space-y-2 z-50"
>
    <template x-for="toast in toasts" :key="toast.id">
        <div
            x-show="toast.visible"
            x-transition:enter="transition ease-out duration-300"
            x-transition:enter-start="opacity-0 translate-x-full"
            x-transition:enter-end="opacity-100 translate-x-0"
            x-transition:leave="transition ease-in duration-200"
            x-transition:leave-start="opacity-100 translate-x-0"
            x-transition:leave-end="opacity-0 translate-x-full"
            :class="{
                'bg-green-500': toast.type === 'success',
                'bg-red-500': toast.type === 'error',
                'bg-blue-500': toast.type === 'info',
                'bg-yellow-500': toast.type === 'warning'
            }"
            class="px-4 py-2 rounded text-white shadow-lg flex items-center gap-2"
        >
            <span x-text="toast.message"></span>
            <button @click="removeToast(toast.id)" class="hover:opacity-75">×</button>
        </div>
    </template>
</div>

<script>
function toastHandler() {
    return {
        toasts: [],

        addToast(detail) {
            const toast = {
                id: Date.now(),
                message: detail.message || '알림',
                type: detail.type || 'info',
                visible: true
            };

            this.toasts.push(toast);

            // 5초 후 자동 제거
            setTimeout(() => {
                this.removeToast(toast.id);
            }, detail.duration || 5000);
        },

        removeToast(id) {
            const toast = this.toasts.find(t => t.id === id);
            if (toast) {
                toast.visible = false;
                setTimeout(() => {
                    this.toasts = this.toasts.filter(t => t.id !== id);
                }, 200);
            }
        }
    };
}
</script>

<!-- 사용 예시 -->
<button @click="$dispatch('show-toast', { message: '저장되었습니다!', type: 'success' })">
    성공 토스트
</button>

<!-- HTMX와 함께 (서버에서 HX-Trigger 헤더 사용) -->
<!-- 서버 응답 헤더: HX-Trigger: {"show-toast": {"message": "저장됨!", "type": "success"}} -->
```

### 14.4 검색 자동완성

```html
<div
    x-data="{
        query: '',
        results: [],
        selectedIndex: -1,
        showResults: false
    }"
    @click.outside="showResults = false"
>
    <input
        type="text"
        x-model.debounce.300ms="query"
        @focus="showResults = true"
        @keydown.arrow-down.prevent="selectedIndex = Math.min(selectedIndex + 1, results.length - 1)"
        @keydown.arrow-up.prevent="selectedIndex = Math.max(selectedIndex - 1, -1)"
        @keydown.enter.prevent="selectItem()"
        @keydown.escape="showResults = false"
        hx-get="/api/search"
        hx-trigger="input changed delay:300ms"
        hx-target="#search-results"
        placeholder="검색어 입력..."
    >

    <!-- HTMX가 결과를 여기에 삽입 -->
    <div
        id="search-results"
        x-show="showResults && query.length > 0"
        x-transition
        class="absolute mt-1 w-full bg-white border rounded shadow-lg"
        @htmx:after-swap="results = [...document.querySelectorAll('#search-results .result-item')]"
    >
        <!-- 서버에서 렌더링된 결과 -->
    </div>
</div>
```

---

## 15. 이 프로젝트의 Alpine.js 활용

### 15.1 다크 모드 토글

```html
<!-- templates/base.html -->
<html
    x-data="{
        darkMode: localStorage.getItem('darkMode') === 'true'
    }"
    x-init="$watch('darkMode', val => localStorage.setItem('darkMode', val))"
    :class="{ 'dark': darkMode }"
>
<head>
    <!-- Tailwind dark mode 설정 -->
    <script>
        // 페이지 깜빡임 방지: HTML 파싱 전에 실행
        if (localStorage.getItem('darkMode') === 'true') {
            document.documentElement.classList.add('dark');
        }
    </script>
</head>
<body class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">

    <!-- 다크 모드 토글 버튼 -->
    <button
        @click="darkMode = !darkMode"
        class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
    >
        <span x-show="!darkMode">🌙</span>
        <span x-show="darkMode">☀️</span>
    </button>

</body>
</html>
```

### 15.2 네비게이션 드롭다운

```html
<nav x-data="{ mobileMenuOpen: false }">
    <!-- 모바일 메뉴 버튼 -->
    <button
        @click="mobileMenuOpen = !mobileMenuOpen"
        class="md:hidden"
    >
        <span x-show="!mobileMenuOpen">☰</span>
        <span x-show="mobileMenuOpen">✕</span>
    </button>

    <!-- 데스크톱 메뉴 -->
    <div class="hidden md:flex">
        <!-- 드롭다운 메뉴 -->
        <div x-data="{ open: false }" class="relative">
            <button @click="open = !open">
                제품 ▼
            </button>
            <div
                x-show="open"
                @click.outside="open = false"
                x-transition
                class="absolute top-full left-0 bg-white shadow-lg rounded"
            >
                <a href="/products/1">제품 1</a>
                <a href="/products/2">제품 2</a>
            </div>
        </div>
    </div>

    <!-- 모바일 메뉴 -->
    <div
        x-show="mobileMenuOpen"
        x-transition
        class="md:hidden"
    >
        <a href="/">홈</a>
        <a href="/products">제품</a>
        <a href="/about">소개</a>
    </div>
</nav>
```

### 15.3 폼 유효성 검사

```html
<form
    x-data="{
        email: '',
        password: '',
        passwordConfirm: '',
        errors: {},
        submitted: false,

        validate() {
            this.errors = {};

            // 이메일 검증
            if (!this.email) {
                this.errors.email = '이메일을 입력하세요';
            } else if (!this.email.includes('@')) {
                this.errors.email = '올바른 이메일 형식이 아닙니다';
            }

            // 비밀번호 검증
            if (!this.password) {
                this.errors.password = '비밀번호를 입력하세요';
            } else if (this.password.length < 8) {
                this.errors.password = '비밀번호는 8자 이상이어야 합니다';
            }

            // 비밀번호 확인
            if (this.password !== this.passwordConfirm) {
                this.errors.passwordConfirm = '비밀번호가 일치하지 않습니다';
            }

            return Object.keys(this.errors).length === 0;
        },

        async submit() {
            this.submitted = true;
            if (!this.validate()) return;

            // HTMX로 제출하거나 여기서 fetch 사용
            this.$el.submit();
        }
    }"
    @submit.prevent="submit()"
    hx-post="/auth/register"
    hx-target="#result"
>
    <div>
        <label>이메일</label>
        <input
            type="email"
            x-model="email"
            @blur="submitted && validate()"
            :class="{ 'border-red-500': errors.email }"
        >
        <p x-show="errors.email" x-text="errors.email" class="text-red-500 text-sm"></p>
    </div>

    <div>
        <label>비밀번호</label>
        <input
            type="password"
            x-model="password"
            @blur="submitted && validate()"
            :class="{ 'border-red-500': errors.password }"
        >
        <p x-show="errors.password" x-text="errors.password" class="text-red-500 text-sm"></p>
    </div>

    <div>
        <label>비밀번호 확인</label>
        <input
            type="password"
            x-model="passwordConfirm"
            @blur="submitted && validate()"
            :class="{ 'border-red-500': errors.passwordConfirm }"
        >
        <p x-show="errors.passwordConfirm" x-text="errors.passwordConfirm" class="text-red-500 text-sm"></p>
    </div>

    <button type="submit">가입하기</button>

    <div id="result"></div>
</form>
```

### 15.4 무한 스크롤

```html
<div
    x-data="{
        page: 1,
        loading: false,
        hasMore: true
    }"
    x-init="
        // 스크롤 감지
        window.addEventListener('scroll', () => {
            if (loading || !hasMore) return;

            const scrollBottom = window.scrollY + window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;

            if (documentHeight - scrollBottom < 200) {
                loadMore();
            }
        });
    "
>
    <!-- 아이템 목록 -->
    <div id="items-list">
        <!-- 서버에서 렌더링된 아이템들 -->
    </div>

    <!-- 더 보기 버튼/로딩 표시 -->
    <div x-show="hasMore" class="text-center py-4">
        <button
            x-show="!loading"
            @click="loadMore()"
            hx-get="/partials/items"
            hx-target="#items-list"
            hx-swap="beforeend"
            :hx-vals="JSON.stringify({ page: page + 1 })"
            @htmx:before-request="loading = true"
            @htmx:after-request="loading = false; page++; checkHasMore()"
        >
            더 보기
        </button>
        <span x-show="loading">로딩 중...</span>
    </div>

    <div x-show="!hasMore" class="text-center py-4 text-gray-500">
        모든 항목을 불러왔습니다
    </div>
</div>
```

---

## 16. 디버깅 팁

### 16.1 개발자 도구 사용

```html
<div x-data="{ count: 0, user: { name: '홍길동' } }">
    <!-- 상태 확인용 (개발 시에만) -->
    <pre x-text="JSON.stringify({ count, user }, null, 2)"></pre>
    <!-- JSON.stringify: 객체를 보기 좋게 출력 -->
    <!-- null, 2: 들여쓰기 2칸 -->

    <button @click="count++">증가</button>
</div>
```

### 16.2 콘솔 로깅

```html
<div
    x-data="{ value: '' }"
    x-effect="console.log('value:', value)"
>
    <!-- x-effect로 값 변화 추적 -->
    <input x-model="value">
</div>

<button @click="console.log('클릭!'); doSomething()">
    <!-- 이벤트 핸들러에서 로깅 -->
</button>
```

### 16.3 일반적인 실수

```html
<!-- ❌ 잘못된 예 -->
<div x-data="{ items: [] }">
    <div x-for="item in items">  <!-- template 태그 없음! -->
        <span x-text="item"></span>
    </div>
</div>

<!-- ✓ 올바른 예 -->
<div x-data="{ items: [] }">
    <template x-for="item in items">
        <div>
            <span x-text="item"></span>
        </div>
    </template>
</div>

<!-- ❌ 잘못된 예: x-if에서 template 없음 -->
<div x-if="show">내용</div>

<!-- ✓ 올바른 예 -->
<template x-if="show">
    <div>내용</div>
</template>

<!-- ❌ 잘못된 예: 문자열 따옴표 -->
<div x-data="{ name: 홍길동 }">  <!-- 따옴표 없음! -->

<!-- ✓ 올바른 예 -->
<div x-data="{ name: '홍길동' }">  <!-- 따옴표 필수 -->
```

---

## 17. 학습 순서 추천

1. **기초** (1주차)
   - x-data: 상태 정의
   - x-text: 텍스트 출력
   - @click: 클릭 이벤트
   - x-show: 조건부 표시

2. **폼 처리** (2주차)
   - x-model: 양방향 바인딩
   - x-bind / `:`: 속성 바인딩
   - 폼 유효성 검사

3. **반복과 조건** (3주차)
   - x-for: 반복 렌더링
   - x-if: 조건부 렌더링
   - :key 사용법

4. **고급 기능** (4주차)
   - x-transition: 애니메이션
   - $dispatch: 이벤트 통신
   - $refs: 요소 참조
   - HTMX 통합

---

## 18. 참고 자료

### 공식 문서
- [Alpine.js 공식 사이트](https://alpinejs.dev)
- [Alpine.js 시작하기](https://alpinejs.dev/start-here)
- [디렉티브 레퍼런스](https://alpinejs.dev/directives/data)
- [매직 프로퍼티](https://alpinejs.dev/magics/el)

### 추가 학습
- [Alpine.js + HTMX 조합](https://htmx.org/essays/alpine-js/)
- [Tailwind CSS와 함께 사용하기](https://tailwindcss.com)

---

## 요약: 핵심 개념 정리

| 디렉티브 | 용도 | 예시 |
|---------|------|------|
| x-data | 상태 정의 | `x-data="{ count: 0 }"` |
| x-text | 텍스트 출력 | `x-text="message"` |
| x-html | HTML 출력 | `x-html="htmlContent"` |
| x-show | 표시/숨김 | `x-show="isVisible"` |
| x-if | DOM 추가/제거 | `<template x-if="show">` |
| x-for | 반복 | `<template x-for="item in items">` |
| x-bind / : | 속성 바인딩 | `:class="{ active: isActive }"` |
| x-model | 양방향 바인딩 | `x-model="inputValue"` |
| x-on / @ | 이벤트 | `@click="handleClick()"` |
| x-transition | 애니메이션 | `x-transition` |
| x-init | 초기화 | `x-init="loadData()"` |
| x-effect | 반응형 효과 | `x-effect="save(data)"` |

| 매직 프로퍼티 | 용도 |
|--------------|------|
| $el | 현재 요소 |
| $refs | 요소 참조 |
| $dispatch | 이벤트 발송 |
| $watch | 변경 감지 |
| $nextTick | DOM 업데이트 후 실행 |
| $event | 이벤트 객체 |
| $store | 전역 스토어 |
