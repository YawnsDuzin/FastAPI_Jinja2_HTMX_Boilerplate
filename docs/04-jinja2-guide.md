# Jinja2 템플릿 가이드

## 1. Jinja2란 무엇인가?

### 1.1 기본 개념

Jinja2는 Python에서 **HTML을 동적으로 생성**하는 템플릿 엔진입니다.

**템플릿 엔진이란?**
```
일반 HTML (정적):
<h1>안녕하세요</h1>
→ 항상 같은 내용만 보여줌

Jinja2 템플릿 (동적):
<h1>안녕하세요, {{ username }}님!</h1>
→ username이 "홍길동"이면 "안녕하세요, 홍길동님!" 표시
→ username이 "김철수"이면 "안녕하세요, 김철수님!" 표시
```

**비유로 이해하기:**
```
템플릿은 "빈칸 채우기 양식"과 같습니다.

일반 편지:
"안녕하세요, ___님! ___에 가입하신 것을 환영합니다."

Jinja2:
"안녕하세요, {{ name }}님! {{ service }}에 가입하신 것을 환영합니다."

Python에서:
name = "홍길동"
service = "쇼핑몰"

결과:
"안녕하세요, 홍길동님! 쇼핑몰에 가입하신 것을 환영합니다."
```

### 1.2 왜 Jinja2를 사용하는가?

| 기능 | 일반 Python 문자열 | Jinja2 |
|------|-------------------|--------|
| 변수 삽입 | f"안녕 {name}" | {{ name }} |
| 반복문 | for문으로 문자열 조합 | {% for %} |
| 조건문 | if문으로 문자열 선택 | {% if %} |
| 보안 | XSS 공격에 취약 | 자동 이스케이프 |
| 템플릿 재사용 | 불가능 | 상속/포함 지원 |

---

## 2. 기본 문법

### 2.1 세 가지 구분 기호

Jinja2에는 세 가지 특별한 구분 기호가 있습니다:

```jinja2
{# ============================================================ #}
{# 1. {{ }} - 변수 출력 (Expression)                             #}
{# ============================================================ #}

{{ variable }}
{# ↑ variable의 값을 HTML에 출력 #}

{# ============================================================ #}
{# 2. {% %} - 로직 실행 (Statement)                             #}
{# ============================================================ #}

{% if condition %}
    ...
{% endif %}
{# ↑ 조건문, 반복문 등 로직 처리 #}

{# ============================================================ #}
{# 3. {# #} - 주석 (Comment)                                    #}
{# ============================================================ #}

{# 이것은 주석입니다. HTML에 출력되지 않습니다. #}
{# ↑ 개발자만 보는 메모 #}
```

**각 기호의 역할 비교:**
```jinja2
{# 이것은 주석 - 아무것도 출력 안됨 #}

{{ "이것은 출력됨" }}
{# 결과: 이것은 출력됨 #}

{% set x = 5 %}
{# 결과: 아무것도 출력 안됨, 하지만 x에 5가 저장됨 #}
```

### 2.2 변수 출력

```jinja2
{# ============================================================ #}
{# 기본 변수 출력                                                #}
{# ============================================================ #}

<p>이름: {{ username }}</p>
{# Python에서 전달한 username 변수의 값을 출력 #}
{# username = "홍길동" → <p>이름: 홍길동</p> #}


{# ============================================================ #}
{# 객체의 속성 접근                                              #}
{# ============================================================ #}

<p>사용자: {{ user.name }}</p>
{# user 객체의 name 속성에 접근 #}
{# user = User(name="김철수") → <p>사용자: 김철수</p> #}

<p>이메일: {{ user['email'] }}</p>
{# 딕셔너리 형태로도 접근 가능 #}
{# user = {"email": "test@test.com"} → <p>이메일: test@test.com</p> #}


{# ============================================================ #}
{# 중첩된 객체 접근                                              #}
{# ============================================================ #}

<p>도시: {{ user.address.city }}</p>
{#
   user = {
       "address": {
           "city": "서울"
       }
   }
   결과: <p>도시: 서울</p>
#}


{# ============================================================ #}
{# 기본값 설정 (변수가 없을 때)                                  #}
{# ============================================================ #}

<p>이름: {{ username | default('손님') }}</p>
{#
   username이 없거나 None이면 '손님' 출력

   username = None → <p>이름: 손님</p>
   username = "홍길동" → <p>이름: 홍길동</p>
#}


{# ============================================================ #}
{# 여러 변수 조합                                                #}
{# ============================================================ #}

<p>{{ first_name }} {{ last_name }}님 환영합니다!</p>
{#
   first_name = "길동"
   last_name = "홍"
   결과: <p>길동 홍님 환영합니다!</p>
#}
```

### 2.3 조건문 (if)

Python의 if문과 비슷하지만, 끝에 `{% endif %}`를 붙여야 합니다.

```jinja2
{# ============================================================ #}
{# 기본 if문                                                     #}
{# ============================================================ #}

{% if user %}
    <p>로그인됨: {{ user.name }}</p>
{% endif %}

{#
   동작 설명:
   - user가 존재하면 (True로 평가되면) 안의 내용 출력
   - user가 None이거나 없으면 아무것도 출력 안됨

   Python으로 비유:
   if user:
       print(f"<p>로그인됨: {user.name}</p>")
#}


{# ============================================================ #}
{# if-else문                                                     #}
{# ============================================================ #}

{% if user.is_authenticated %}
    <p>환영합니다, {{ user.name }}님!</p>
    <a href="/logout">로그아웃</a>
{% else %}
    <p>로그인이 필요합니다.</p>
    <a href="/login">로그인</a>
{% endif %}

{#
   is_authenticated가 True면:
   → "환영합니다, 홍길동님!" + 로그아웃 링크

   is_authenticated가 False면:
   → "로그인이 필요합니다." + 로그인 링크
#}


{# ============================================================ #}
{# if-elif-else문                                                #}
{# ============================================================ #}

{% if user.role == 'admin' %}
    <span class="badge badge-red">관리자</span>
{% elif user.role == 'moderator' %}
    <span class="badge badge-yellow">운영자</span>
{% elif user.role == 'member' %}
    <span class="badge badge-green">회원</span>
{% else %}
    <span class="badge badge-gray">게스트</span>
{% endif %}

{#
   role에 따라 다른 배지 표시:
   - 'admin' → 빨간 "관리자" 배지
   - 'moderator' → 노란 "운영자" 배지
   - 'member' → 초록 "회원" 배지
   - 그 외 → 회색 "게스트" 배지
#}


{# ============================================================ #}
{# 한 줄 조건문 (인라인 if)                                      #}
{# ============================================================ #}

<button class="{{ 'btn-primary' if is_active else 'btn-secondary' }}">
    버튼
</button>

{#
   Python의 삼항 연산자와 동일:
   'btn-primary' if is_active else 'btn-secondary'

   is_active = True → class="btn-primary"
   is_active = False → class="btn-secondary"
#}


{# ============================================================ #}
{# 복합 조건                                                     #}
{# ============================================================ #}

{% if user and user.is_active and user.email_verified %}
    <p>인증된 활성 사용자입니다.</p>
{% endif %}

{#
   and: 모든 조건이 True여야 함
   or: 하나라도 True면 됨
   not: 조건 반전
#}

{% if not user.is_banned and (user.role == 'admin' or user.role == 'moderator') %}
    <a href="/admin">관리 페이지</a>
{% endif %}

{#
   - 차단되지 않았고
   - 관리자이거나 운영자이면
   → 관리 페이지 링크 표시
#}
```

### 2.4 반복문 (for)

```jinja2
{# ============================================================ #}
{# 기본 for문                                                    #}
{# ============================================================ #}

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>

{#
   items = ["사과", "바나나", "체리"]

   결과:
   <ul>
       <li>사과</li>
       <li>바나나</li>
       <li>체리</li>
   </ul>
#}


{# ============================================================ #}
{# 빈 목록 처리 (else)                                           #}
{# ============================================================ #}

<ul>
{% for item in items %}
    <li>{{ item.name }}</li>
{% else %}
    <li>아이템이 없습니다.</li>
{% endfor %}
</ul>

{#
   items가 빈 리스트 []이면:
   <ul>
       <li>아이템이 없습니다.</li>
   </ul>

   items = [{"name": "사과"}] 이면:
   <ul>
       <li>사과</li>
   </ul>
#}


{# ============================================================ #}
{# 객체 리스트 반복                                              #}
{# ============================================================ #}

{% for product in products %}
<div class="product-card">
    <h3>{{ product.name }}</h3>
    <p>가격: {{ product.price }}원</p>
    <p>{{ product.description }}</p>
</div>
{% endfor %}

{#
   products = [
       {"name": "노트북", "price": 1500000, "description": "맥북 프로"},
       {"name": "마우스", "price": 50000, "description": "무선 마우스"}
   ]

   결과:
   <div class="product-card">
       <h3>노트북</h3>
       <p>가격: 1500000원</p>
       <p>맥북 프로</p>
   </div>
   <div class="product-card">
       <h3>마우스</h3>
       <p>가격: 50000원</p>
       <p>무선 마우스</p>
   </div>
#}


{# ============================================================ #}
{# loop 변수 (반복문 내장 변수)                                   #}
{# ============================================================ #}

{% for user in users %}
<tr class="{{ 'bg-gray-100' if loop.index is odd else '' }}">
    {# loop.index: 1부터 시작하는 순번 #}
    <td>{{ loop.index }}</td>

    {# loop.index0: 0부터 시작하는 순번 #}
    <td>인덱스: {{ loop.index0 }}</td>

    <td>{{ user.name }}</td>

    {# loop.first: 첫 번째 항목인지 (True/False) #}
    {% if loop.first %}
        <td><span class="badge">첫 번째</span></td>
    {% endif %}

    {# loop.last: 마지막 항목인지 (True/False) #}
    {% if loop.last %}
        <td><span class="badge">마지막</span></td>
    {% endif %}
</tr>
{% endfor %}

{#
   사용 가능한 loop 변수들:

   loop.index     - 1부터 시작하는 현재 순번
   loop.index0    - 0부터 시작하는 현재 순번
   loop.revindex  - 끝에서부터 세는 순번 (1부터)
   loop.revindex0 - 끝에서부터 세는 순번 (0부터)
   loop.first     - 첫 번째 항목이면 True
   loop.last      - 마지막 항목이면 True
   loop.length    - 전체 항목 수
   loop.cycle     - 값들을 순환하며 출력
#}


{# ============================================================ #}
{# loop.cycle 사용 예시                                          #}
{# ============================================================ #}

{% for item in items %}
<tr class="{{ loop.cycle('bg-white', 'bg-gray-100') }}">
    {# 홀수 행은 흰색, 짝수 행은 회색 #}
    <td>{{ item }}</td>
</tr>
{% endfor %}

{#
   결과:
   <tr class="bg-white"><td>첫번째</td></tr>
   <tr class="bg-gray-100"><td>두번째</td></tr>
   <tr class="bg-white"><td>세번째</td></tr>
   <tr class="bg-gray-100"><td>네번째</td></tr>
   ...
#}


{# ============================================================ #}
{# 딕셔너리 반복                                                 #}
{# ============================================================ #}

{% for key, value in user.items() %}
<p>{{ key }}: {{ value }}</p>
{% endfor %}

{#
   user = {"name": "홍길동", "age": 30, "city": "서울"}

   결과:
   <p>name: 홍길동</p>
   <p>age: 30</p>
   <p>city: 서울</p>
#}


{# ============================================================ #}
{# 중첩 반복문                                                   #}
{# ============================================================ #}

{% for category in categories %}
<h2>{{ category.name }}</h2>
<ul>
    {% for product in category.products %}
    <li>{{ product.name }} - {{ product.price }}원</li>
    {% endfor %}
</ul>
{% endfor %}

{#
   categories = [
       {
           "name": "전자제품",
           "products": [
               {"name": "노트북", "price": 1500000},
               {"name": "마우스", "price": 50000}
           ]
       },
       {
           "name": "식품",
           "products": [
               {"name": "사과", "price": 3000}
           ]
       }
   ]

   결과:
   <h2>전자제품</h2>
   <ul>
       <li>노트북 - 1500000원</li>
       <li>마우스 - 50000원</li>
   </ul>
   <h2>식품</h2>
   <ul>
       <li>사과 - 3000원</li>
   </ul>
#}
```

---

## 3. 필터 (Filters)

필터는 변수를 출력하기 전에 변환하는 기능입니다. `|` (파이프) 기호를 사용합니다.

### 3.1 문자열 필터

```jinja2
{# ============================================================ #}
{# 대소문자 변환                                                 #}
{# ============================================================ #}

{{ "hello world" | upper }}
{# 결과: HELLO WORLD #}
{# 모든 글자를 대문자로 변환 #}

{{ "HELLO WORLD" | lower }}
{# 결과: hello world #}
{# 모든 글자를 소문자로 변환 #}

{{ "hello world" | capitalize }}
{# 결과: Hello world #}
{# 첫 글자만 대문자로 변환 #}

{{ "hello world" | title }}
{# 결과: Hello World #}
{# 각 단어의 첫 글자를 대문자로 변환 #}


{# ============================================================ #}
{# 공백 처리                                                    #}
{# ============================================================ #}

{{ "  hello world  " | trim }}
{# 결과: hello world #}
{# 앞뒤 공백 제거 #}


{# ============================================================ #}
{# 문자열 자르기                                                 #}
{# ============================================================ #}

{{ "이것은 아주 긴 문장입니다. 이 문장을 줄여야 합니다." | truncate(20) }}
{# 결과: 이것은 아주 긴 문장입니다... #}
{# 20자로 자르고 ... 추가 #}

{{ "안녕하세요 여러분" | truncate(10, killwords=False) }}
{# 결과: 안녕하세요... #}
{# killwords=False: 단어 중간에서 자르지 않음 #}

{{ "안녕하세요 여러분" | truncate(10, end='>>>') }}
{# 결과: 안녕하세요>>> #}
{# end: 잘린 부분 표시 기호 변경 #}


{# ============================================================ #}
{# 문자열 치환                                                   #}
{# ============================================================ #}

{{ "Hello World" | replace("World", "Python") }}
{# 결과: Hello Python #}


{# ============================================================ #}
{# 문자열 길이                                                   #}
{# ============================================================ #}

{{ "안녕하세요" | length }}
{# 결과: 5 #}
{# 문자열의 글자 수 반환 #}
```

### 3.2 숫자 필터

```jinja2
{# ============================================================ #}
{# 반올림                                                        #}
{# ============================================================ #}

{{ 3.14159 | round }}
{# 결과: 3.0 #}
{# 소수점 첫째 자리에서 반올림 #}

{{ 3.14159 | round(2) }}
{# 결과: 3.14 #}
{# 소수점 둘째 자리까지 표시 #}

{{ 3.5 | round(0, 'floor') }}
{# 결과: 3 #}
{# 버림 #}

{{ 3.1 | round(0, 'ceil') }}
{# 결과: 4 #}
{# 올림 #}


{# ============================================================ #}
{# 절대값                                                        #}
{# ============================================================ #}

{{ -5 | abs }}
{# 결과: 5 #}


{# ============================================================ #}
{# 숫자 포맷팅 (커스텀 필터로 구현)                              #}
{# ============================================================ #}

{{ 1234567 | format('{:,}') }}
{# 결과: 1,234,567 #}
{# 천 단위 콤마 (프로젝트에서 커스텀 필터로 구현해야 함) #}
```

### 3.3 리스트 필터

```jinja2
{# ============================================================ #}
{# 리스트 길이                                                   #}
{# ============================================================ #}

{{ items | length }}
{# items = [1, 2, 3, 4, 5] → 5 #}


{# ============================================================ #}
{# 첫 번째/마지막 항목                                           #}
{# ============================================================ #}

{{ items | first }}
{# items = ["사과", "바나나", "체리"] → 사과 #}

{{ items | last }}
{# items = ["사과", "바나나", "체리"] → 체리 #}


{# ============================================================ #}
{# 리스트를 문자열로 합치기                                      #}
{# ============================================================ #}

{{ items | join(', ') }}
{# items = ["사과", "바나나", "체리"] → 사과, 바나나, 체리 #}

{{ items | join(' | ') }}
{# items = ["사과", "바나나", "체리"] → 사과 | 바나나 | 체리 #}


{# ============================================================ #}
{# 정렬                                                          #}
{# ============================================================ #}

{{ items | sort }}
{# items = [3, 1, 2] → [1, 2, 3] #}

{{ items | sort(reverse=true) }}
{# items = [1, 2, 3] → [3, 2, 1] #}

{{ users | sort(attribute='name') }}
{# users를 name 속성으로 정렬 #}


{# ============================================================ #}
{# 역순                                                          #}
{# ============================================================ #}

{{ items | reverse | list }}
{# items = [1, 2, 3] → [3, 2, 1] #}


{# ============================================================ #}
{# 유니크 (중복 제거)                                            #}
{# ============================================================ #}

{{ items | unique | list }}
{# items = [1, 2, 2, 3, 3, 3] → [1, 2, 3] #}


{# ============================================================ #}
{# 합계                                                          #}
{# ============================================================ #}

{{ items | sum }}
{# items = [10, 20, 30] → 60 #}

{{ products | sum(attribute='price') }}
{# products의 price 필드 합계 #}
```

### 3.4 날짜/시간 필터 (커스텀)

이 프로젝트에서 정의된 커스텀 필터입니다.

```jinja2
{# ============================================================ #}
{# 날짜/시간 포맷팅                                              #}
{# ============================================================ #}

{{ created_at | datetime }}
{# 결과: 2024-01-15 14:30 (기본 포맷) #}

{{ created_at | datetime('%Y년 %m월 %d일') }}
{# 결과: 2024년 01월 15일 #}

{{ created_at | datetime('%Y-%m-%d %H:%M:%S') }}
{# 결과: 2024-01-15 14:30:45 #}


{# ============================================================ #}
{# 상대 시간 (예: "3시간 전")                                    #}
{# ============================================================ #}

{{ created_at | timeago }}
{# 결과: 3시간 전 #}


{# ============================================================ #}
{# 통화 포맷팅                                                   #}
{# ============================================================ #}

{{ price | currency }}
{# price = 15000 → ₩15,000 #}

{{ price | currency('$') }}
{# price = 100 → $100 #}
```

### 3.5 HTML 관련 필터

```jinja2
{# ============================================================ #}
{# safe 필터 - HTML 이스케이프 비활성화                          #}
{# ============================================================ #}

{# 기본 동작: HTML 이스케이프됨 (안전) #}
{{ html_content }}
{# html_content = "<b>굵은 글씨</b>" #}
{# 결과: &lt;b&gt;굵은 글씨&lt;/b&gt; (태그가 그대로 보임) #}

{# safe 필터: 이스케이프 비활성화 (위험!) #}
{{ html_content | safe }}
{# 결과: <b>굵은 글씨</b> (태그가 적용됨) #}

{# 경고:
   사용자 입력에는 절대 safe 필터를 사용하지 마세요!
   XSS 공격에 취약해집니다.

   safe 필터는 다음과 같은 신뢰할 수 있는 HTML에만 사용:
   - 관리자가 작성한 콘텐츠
   - 마크다운을 HTML로 변환한 결과
   - 프로그램에서 생성한 HTML
#}


{# ============================================================ #}
{# striptags - HTML 태그 제거                                    #}
{# ============================================================ #}

{{ html_content | striptags }}
{# html_content = "<p><b>안녕</b>하세요</p>" #}
{# 결과: 안녕하세요 #}


{# ============================================================ #}
{# escape - 명시적 이스케이프                                    #}
{# ============================================================ #}

{{ user_input | escape }}
{# user_input = "<script>alert('hack')</script>" #}
{# 결과: &lt;script&gt;alert('hack')&lt;/script&gt; #}
{# → 스크립트가 실행되지 않고 텍스트로 표시됨 #}
```

### 3.6 필터 체인

여러 필터를 연결해서 사용할 수 있습니다.

```jinja2
{# ============================================================ #}
{# 필터 체인 (여러 필터 연속 적용)                               #}
{# ============================================================ #}

{{ "  hello world  " | trim | upper }}
{# 1단계: "  hello world  " | trim → "hello world" #}
{# 2단계: "hello world" | upper → "HELLO WORLD" #}
{# 결과: HELLO WORLD #}


{{ description | truncate(100) | lower }}
{# 1단계: 100자로 자름 #}
{# 2단계: 소문자로 변환 #}


{{ items | sort | first }}
{# 1단계: 정렬 #}
{# 2단계: 첫 번째 항목 가져오기 #}


{{ users | selectattr('is_active') | list | length }}
{# 1단계: is_active가 True인 사용자만 선택 #}
{# 2단계: 리스트로 변환 #}
{# 3단계: 개수 계산 #}
```

---

## 4. 템플릿 상속 (Template Inheritance)

템플릿 상속은 Jinja2의 가장 강력한 기능 중 하나입니다.

### 4.1 기본 개념

```
상속의 비유:

부모 템플릿 (base.html):
┌─────────────────────────┐
│ 헤더 (모든 페이지 동일) │
├─────────────────────────┤
│                         │
│   내용 영역 (빈 칸)     │  ← 자식이 채울 부분
│                         │
├─────────────────────────┤
│ 푸터 (모든 페이지 동일) │
└─────────────────────────┘

자식 템플릿 (home.html):
"부모 템플릿을 기반으로 하되,
 내용 영역만 내가 원하는 걸로 채울게!"

결과:
┌─────────────────────────┐
│ 헤더 (부모에서 상속)    │
├─────────────────────────┤
│                         │
│   홈페이지 내용         │  ← 자식이 채운 부분
│                         │
├─────────────────────────┤
│ 푸터 (부모에서 상속)    │
└─────────────────────────┘
```

### 4.2 부모 템플릿 만들기

```jinja2
{# templates/base.html #}

<!DOCTYPE html>
<html lang="ko">
<head>
    {# ============================================================ #}
    {# 기본 메타 태그                                                #}
    {# ============================================================ #}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {# ============================================================ #}
    {# title 블록: 자식이 재정의 가능한 영역                         #}
    {# ============================================================ #}
    <title>{% block title %}{{ app_name }}{% endblock %}</title>
    {#
       {% block 이름 %} ... {% endblock %}
       → 자식 템플릿이 이 부분을 다른 내용으로 교체할 수 있음

       {{ app_name }}
       → 자식이 title 블록을 정의하지 않으면 app_name이 표시됨 (기본값)
    #}

    {# ============================================================ #}
    {# 기본 CSS/JS (모든 페이지에 포함)                              #}
    {# ============================================================ #}
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>

    {# ============================================================ #}
    {# extra_head 블록: 페이지별 추가 CSS/JS                         #}
    {# ============================================================ #}
    {% block extra_head %}{% endblock %}
    {#
       빈 블록: 자식이 필요시 추가 내용을 넣을 수 있음
       자식이 정의하지 않으면 아무것도 출력 안됨
    #}
</head>

<body class="bg-gray-100">
    {# ============================================================ #}
    {# 네비게이션 바 (모든 페이지에 동일)                            #}
    {# ============================================================ #}
    {% include "components/navbar.html" %}
    {#
       {% include "파일경로" %}
       → 다른 템플릿 파일의 내용을 이 위치에 삽입
       → navbar.html의 내용이 여기에 들어감
    #}

    {# ============================================================ #}
    {# 메인 콘텐츠 영역                                              #}
    {# ============================================================ #}
    <main class="container mx-auto py-8">
        {% block content %}{% endblock %}
        {#
           이 블록이 각 페이지의 주요 내용이 들어갈 곳
           자식 템플릿에서 반드시 정의해야 함
        #}
    </main>

    {# ============================================================ #}
    {# 푸터 (모든 페이지에 동일)                                     #}
    {# ============================================================ #}
    {% include "components/footer.html" %}

    {# ============================================================ #}
    {# extra_scripts 블록: 페이지별 추가 스크립트                    #}
    {# ============================================================ #}
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### 4.3 자식 템플릿 만들기

```jinja2
{# templates/pages/home.html #}

{# ============================================================ #}
{# 부모 템플릿 상속                                              #}
{# ============================================================ #}
{% extends "base.html" %}
{#
   {% extends "파일경로" %}
   → 이 템플릿은 base.html을 기반으로 함
   → base.html의 모든 내용을 상속받음

   주의: extends는 반드시 파일의 첫 줄에 와야 함!
#}

{# ============================================================ #}
{# title 블록 재정의                                             #}
{# ============================================================ #}
{% block title %}홈 | {{ app_name }}{% endblock %}
{#
   부모의 title 블록을 덮어씀
   결과: <title>홈 | 앱이름</title>
#}

{# ============================================================ #}
{# content 블록 재정의                                           #}
{# ============================================================ #}
{% block content %}
<div class="text-center">
    <h1 class="text-4xl font-bold mb-4">환영합니다!</h1>
    <p class="text-gray-600">FastAPI + Jinja2 + HTMX 보일러플레이트</p>

    <div class="mt-8">
        <a href="/login" class="btn btn-primary">로그인</a>
        <a href="/register" class="btn btn-secondary">회원가입</a>
    </div>
</div>
{% endblock %}
{#
   부모의 content 블록을 이 내용으로 교체

   최종 결과:
   <!DOCTYPE html>
   <html lang="ko">
   <head>
       ... (부모에서 상속)
       <title>홈 | 앱이름</title>  ← 재정의됨
       ... (부모에서 상속)
   </head>
   <body>
       [네비게이션 바] (부모에서 상속)
       <main>
           [위의 content 내용]  ← 재정의됨
       </main>
       [푸터] (부모에서 상속)
   </body>
   </html>
#}

{# ============================================================ #}
{# 페이지 전용 스크립트 추가                                     #}
{# ============================================================ #}
{% block extra_scripts %}
<script>
    console.log('홈페이지 로드됨');
</script>
{% endblock %}
```

### 4.4 super() 사용하기

부모 블록의 내용을 유지하면서 추가하고 싶을 때 사용합니다.

```jinja2
{# 부모 템플릿 (base.html) #}
{% block sidebar %}
<nav>
    <a href="/">홈</a>
    <a href="/about">소개</a>
</nav>
{% endblock %}


{# 자식 템플릿 (admin.html) #}
{% block sidebar %}
{{ super() }}
{#
   super(): 부모 블록의 내용을 먼저 출력

   결과:
   <nav>
       <a href="/">홈</a>
       <a href="/about">소개</a>
   </nav>
#}

{# 추가 메뉴 #}
<nav>
    <a href="/admin/users">사용자 관리</a>
    <a href="/admin/settings">설정</a>
</nav>
{% endblock %}

{#
   최종 결과:
   <nav>
       <a href="/">홈</a>
       <a href="/about">소개</a>
   </nav>
   <nav>
       <a href="/admin/users">사용자 관리</a>
       <a href="/admin/settings">설정</a>
   </nav>
#}
```

---

## 5. Include와 매크로

### 5.1 Include (템플릿 포함)

다른 템플릿 파일을 현재 위치에 삽입합니다.

```jinja2
{# ============================================================ #}
{# 기본 include                                                  #}
{# ============================================================ #}

{% include "components/navbar.html" %}
{# components/navbar.html의 내용이 여기에 삽입됨 #}


{# ============================================================ #}
{# 변수와 함께 include                                           #}
{# ============================================================ #}

{% include "components/card.html" %}
{#
   card.html에서 현재 컨텍스트의 모든 변수 사용 가능
   (title, description 등)
#}


{# ============================================================ #}
{# 파일이 없을 때 무시                                           #}
{# ============================================================ #}

{% include "components/optional.html" ignore missing %}
{#
   파일이 없어도 에러 발생 안 함
   조건부로 컴포넌트를 포함할 때 유용
#}


{# ============================================================ #}
{# 여러 파일 중 첫 번째로 존재하는 것 사용                        #}
{# ============================================================ #}

{% include ['custom/navbar.html', 'components/navbar.html'] ignore missing %}
{#
   custom/navbar.html이 있으면 사용
   없으면 components/navbar.html 사용
   둘 다 없으면 무시
#}
```

### 5.2 매크로 (Macros)

매크로는 **재사용 가능한 HTML 조각**을 함수처럼 정의하는 기능입니다.

```jinja2
{# ============================================================ #}
{# templates/macros/forms.html - 매크로 정의 파일                #}
{# ============================================================ #}

{# 입력 필드 매크로 #}
{% macro input(name, type='text', value='', label='', required=false, placeholder='') %}
{#
   macro 이름(매개변수들):
   - name: 필수 매개변수
   - type='text': 기본값이 있는 매개변수
   - required=false: 불리언 매개변수
#}

<div class="form-group mb-4">
    {# 라벨이 있으면 표시 #}
    {% if label %}
    <label for="{{ name }}" class="block text-sm font-medium text-gray-700 mb-1">
        {{ label }}
        {% if required %}<span class="text-red-500">*</span>{% endif %}
    </label>
    {% endif %}

    {# 입력 필드 #}
    <input
        type="{{ type }}"
        name="{{ name }}"
        id="{{ name }}"
        value="{{ value }}"
        placeholder="{{ placeholder }}"
        class="w-full px-3 py-2 border border-gray-300 rounded-md
               focus:outline-none focus:ring-2 focus:ring-blue-500"
        {% if required %}required{% endif %}
    >
</div>
{% endmacro %}
{# endmacro로 매크로 정의 끝 #}


{# 버튼 매크로 #}
{% macro button(text, type='submit', variant='primary', size='md') %}
<button
    type="{{ type }}"
    class="btn btn-{{ variant }} btn-{{ size }}"
>
    {{ text }}
</button>
{% endmacro %}


{# 카드 매크로 #}
{% macro card(title, content, footer=none) %}
<div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div class="p-4 border-b">
        <h3 class="text-lg font-semibold">{{ title }}</h3>
    </div>
    <div class="p-4">
        {{ content }}
    </div>
    {% if footer %}
    <div class="p-4 bg-gray-50 border-t">
        {{ footer }}
    </div>
    {% endif %}
</div>
{% endmacro %}
```

### 5.3 매크로 사용하기

```jinja2
{# templates/pages/login.html #}

{% extends "base.html" %}

{# ============================================================ #}
{# 매크로 가져오기                                               #}
{# ============================================================ #}
{% from "macros/forms.html" import input, button %}
{#
   from "파일경로" import 매크로이름
   → 해당 파일에서 특정 매크로만 가져옴
   → Python의 from ... import ...와 동일
#}

{% block content %}
<div class="max-w-md mx-auto">
    <h1 class="text-2xl font-bold mb-6">로그인</h1>

    <form method="post" action="/login">
        {# ============================================================ #}
        {# 매크로 호출                                                   #}
        {# ============================================================ #}

        {{ input(
            name='email',
            type='email',
            label='이메일',
            required=true,
            placeholder='your@email.com'
        ) }}
        {#
           input 매크로 호출
           → 정의된 HTML이 이 위치에 렌더링됨

           결과:
           <div class="form-group mb-4">
               <label for="email" class="...">
                   이메일<span class="text-red-500">*</span>
               </label>
               <input type="email" name="email" id="email"
                      placeholder="your@email.com" required ...>
           </div>
        #}

        {{ input(
            name='password',
            type='password',
            label='비밀번호',
            required=true
        ) }}

        <div class="flex justify-between items-center mt-6">
            {{ button('로그인', type='submit', variant='primary') }}
            <a href="/forgot-password" class="text-sm text-blue-600">
                비밀번호를 잊으셨나요?
            </a>
        </div>
    </form>
</div>
{% endblock %}
```

### 5.4 매크로 내에서 caller() 사용

매크로를 블록처럼 사용할 수 있게 해줍니다.

```jinja2
{# 매크로 정의 #}
{% macro modal(title, id='modal') %}
<div id="{{ id }}" class="modal hidden">
    <div class="modal-overlay"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h2>{{ title }}</h2>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            {{ caller() }}
            {#
               caller(): 매크로를 호출할 때
               {% call %}...{% endcall %} 사이의 내용이 들어감
            #}
        </div>
    </div>
</div>
{% endmacro %}


{# 매크로 사용 #}
{% call modal('삭제 확인', id='delete-modal') %}
    <p>정말로 이 항목을 삭제하시겠습니까?</p>
    <p class="text-red-500">이 작업은 되돌릴 수 없습니다.</p>
    <div class="mt-4">
        <button class="btn btn-danger">삭제</button>
        <button class="btn btn-secondary modal-close">취소</button>
    </div>
{% endcall %}

{#
   결과:
   <div id="delete-modal" class="modal hidden">
       <div class="modal-overlay"></div>
       <div class="modal-content">
           <div class="modal-header">
               <h2>삭제 확인</h2>
               <button class="modal-close">&times;</button>
           </div>
           <div class="modal-body">
               <p>정말로 이 항목을 삭제하시겠습니까?</p>
               <p class="text-red-500">이 작업은 되돌릴 수 없습니다.</p>
               <div class="mt-4">
                   <button class="btn btn-danger">삭제</button>
                   <button class="btn btn-secondary modal-close">취소</button>
               </div>
           </div>
       </div>
   </div>
#}
```

---

## 6. 이 프로젝트의 템플릿 구조

### 6.1 디렉토리 구조

```
templates/
├── base.html               # 기본 레이아웃 (모든 페이지의 부모)
│
├── components/             # 재사용 가능한 컴포넌트
│   ├── navbar.html         # 상단 네비게이션 바
│   ├── footer.html         # 하단 푸터
│   ├── sidebar.html        # 사이드바 메뉴
│   ├── modal.html          # 모달 컨테이너
│   └── toast.html          # 토스트 알림 컨테이너
│
├── macros/                 # 매크로 모음
│   ├── forms.html          # 폼 관련 매크로
│   └── ui.html             # UI 컴포넌트 매크로
│
├── pages/                  # 전체 페이지 템플릿
│   ├── home.html           # 홈페이지
│   ├── login.html          # 로그인 페이지
│   ├── register.html       # 회원가입 페이지
│   ├── dashboard.html      # 대시보드
│   └── items/
│       ├── list.html       # 아이템 목록 페이지
│       └── detail.html     # 아이템 상세 페이지
│
└── partials/               # HTMX용 부분 템플릿
    ├── items/
    │   ├── list.html       # 아이템 목록 (부분)
    │   ├── item.html       # 단일 아이템 카드
    │   ├── form.html       # 아이템 폼
    │   └── empty.html      # 빈 상태 표시
    │
    ├── modals/
    │   ├── confirm.html    # 확인 모달
    │   └── form.html       # 폼 모달
    │
    └── toasts/
        ├── success.html    # 성공 토스트
        ├── error.html      # 에러 토스트
        └── info.html       # 정보 토스트
```

### 6.2 base.html 상세 설명

```jinja2
{# templates/base.html #}

<!DOCTYPE html>
<html lang="ko" x-data="{ darkMode: false }" :class="{ 'dark': darkMode }">
{#
   x-data="{ darkMode: false }": Alpine.js 상태 정의
   :class="{ 'dark': darkMode }": 다크모드 시 'dark' 클래스 추가
#}

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    {# 제목 블록 #}
    <title>{% block title %}{{ app_name }}{% endblock %}</title>

    {# 기본 스타일 #}
    <script src="https://cdn.tailwindcss.com"></script>

    {# HTMX - 부분 업데이트를 위한 라이브러리 #}
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>

    {# Alpine.js - 클라이언트 상호작용을 위한 라이브러리 #}
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>

    {# 페이지별 추가 헤더 #}
    {% block extra_head %}{% endblock %}
</head>

<body hx-boost="true" class="min-h-screen bg-gray-100 dark:bg-gray-900">
    {#
       hx-boost="true": 모든 링크와 폼을 AJAX로 처리
       → 페이지 전체가 아닌 body 내용만 교체됨 (빠른 탐색)
    #}

    {# ============================================================ #}
    {# 토스트 알림 컨테이너 (HTMX 이벤트로 제어)                     #}
    {# ============================================================ #}
    <div id="toast-container"
         class="fixed top-4 right-4 z-50 flex flex-col gap-2"
         x-data="toastHandler()"
         @showToast.window="show($event.detail)">
    </div>

    {# ============================================================ #}
    {# 모달 컨테이너 (HTMX가 내용 삽입)                              #}
    {# ============================================================ #}
    <div id="modal-container"
         x-data="{ open: false }"
         @openModal.window="open = true"
         @closeModal.window="open = false"
         @keydown.escape.window="open = false">

        {# 모달 배경 #}
        <div x-show="open"
             x-transition:enter="transition ease-out duration-200"
             x-transition:leave="transition ease-in duration-150"
             class="fixed inset-0 bg-black/50 z-40"
             @click="open = false">
        </div>

        {# 모달 내용 (HTMX가 여기에 삽입) #}
        <div id="modal-content"
             x-show="open"
             x-transition
             class="fixed inset-0 flex items-center justify-center z-50 p-4">
        </div>
    </div>

    {# ============================================================ #}
    {# 네비게이션 바                                                 #}
    {# ============================================================ #}
    {% include "components/navbar.html" %}

    {# ============================================================ #}
    {# 메인 콘텐츠                                                   #}
    {# ============================================================ #}
    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    {# ============================================================ #}
    {# 푸터                                                          #}
    {# ============================================================ #}
    {% include "components/footer.html" %}

    {# ============================================================ #}
    {# 토스트 핸들러 스크립트                                        #}
    {# ============================================================ #}
    <script>
    function toastHandler() {
        return {
            toasts: [],
            show(detail) {
                const toast = { id: Date.now(), ...detail };
                this.toasts.push(toast);
                setTimeout(() => this.remove(toast.id), 5000);
            },
            remove(id) {
                this.toasts = this.toasts.filter(t => t.id !== id);
            }
        };
    }
    </script>

    {# 페이지별 추가 스크립트 #}
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### 6.3 HTMX 파셜 템플릿 예제

```jinja2
{# templates/partials/items/item.html #}
{#
   단일 아이템 카드 - HTMX로 개별 업데이트/삭제 가능

   필요한 변수:
   - item: 아이템 객체 (id, title, description, created_at 등)
#}

<div id="item-{{ item.id }}"
     class="bg-white rounded-lg shadow p-4 mb-4">
    {#
       id="item-{{ item.id }}":
       → 각 아이템에 고유 ID 부여
       → HTMX가 이 ID로 특정 아이템만 업데이트/삭제 가능
    #}

    <div class="flex justify-between items-start">
        {# 아이템 내용 #}
        <div>
            <h3 class="text-lg font-semibold">{{ item.title }}</h3>
            {% if item.description %}
            <p class="text-gray-600 mt-1">{{ item.description }}</p>
            {% endif %}
            <p class="text-sm text-gray-400 mt-2">
                {{ item.created_at | datetime }}
            </p>
        </div>

        {# 액션 버튼들 #}
        <div class="flex gap-2">
            {# 수정 버튼 #}
            <button
                hx-get="/partials/items/{{ item.id }}/edit"
                hx-target="#modal-content"
                hx-swap="innerHTML"
                @click="$dispatch('openModal')"
                class="btn btn-sm btn-secondary">
                수정
            </button>
            {#
               hx-get: 이 URL로 GET 요청
               hx-target: 응답을 이 요소에 삽입
               hx-swap: innerHTML로 내부 내용 교체
               @click: Alpine.js로 모달 열기 이벤트 발생
            #}

            {# 삭제 버튼 #}
            <button
                hx-delete="/partials/items/{{ item.id }}"
                hx-target="#item-{{ item.id }}"
                hx-swap="outerHTML"
                hx-confirm="정말 삭제하시겠습니까?"
                class="btn btn-sm btn-danger">
                삭제
            </button>
            {#
               hx-delete: DELETE 요청
               hx-target: 이 아이템 카드 자체를 타겟
               hx-swap="outerHTML": 요소 전체를 응답으로 교체
               → 서버가 빈 응답을 주면 아이템 카드가 사라짐
               hx-confirm: 삭제 전 확인 대화상자
            #}
        </div>
    </div>
</div>
```

---

## 7. 커스텀 필터와 전역 변수

### 7.1 커스텀 필터 정의 (Python)

```python
# app/core/templates.py

from datetime import datetime
from fastapi.templating import Jinja2Templates

# Jinja2 템플릿 엔진 설정
templates = Jinja2Templates(directory="templates")

# ============================================================
# 커스텀 필터 정의
# ============================================================

def format_datetime(value, format="%Y-%m-%d %H:%M"):
    """
    날짜/시간을 포맷팅하는 필터

    사용법: {{ created_at | datetime }}
            {{ created_at | datetime('%Y년 %m월 %d일') }}
    """
    if value is None:
        return ""
    return value.strftime(format)


def format_currency(value, symbol="₩"):
    """
    숫자를 통화 형식으로 포맷팅하는 필터

    사용법: {{ price | currency }}
            {{ price | currency('$') }}
    """
    if value is None:
        return ""
    return f"{symbol}{value:,.0f}"


def format_timeago(value):
    """
    상대 시간을 표시하는 필터

    사용법: {{ created_at | timeago }}
    결과: "3시간 전", "2일 전" 등
    """
    if value is None:
        return ""

    now = datetime.now(value.tzinfo)
    diff = now - value

    seconds = diff.total_seconds()

    if seconds < 60:
        return "방금 전"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}분 전"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}시간 전"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days}일 전"
    else:
        return value.strftime("%Y-%m-%d")


# ============================================================
# 필터 등록
# ============================================================
templates.env.filters["datetime"] = format_datetime
templates.env.filters["currency"] = format_currency
templates.env.filters["timeago"] = format_timeago
#
# templates.env.filters["필터이름"] = 함수
# → 템플릿에서 {{ 변수 | 필터이름 }} 형태로 사용 가능
```

### 7.2 전역 변수 등록

```python
# app/core/templates.py (계속)

from app.core.config import settings

# ============================================================
# 전역 변수 등록
# ============================================================

templates.env.globals["app_name"] = settings.app_name
# → 모든 템플릿에서 {{ app_name }} 사용 가능

templates.env.globals["now"] = datetime.now
# → 모든 템플릿에서 {{ now() }} 사용 가능
# → 함수도 등록 가능!

templates.env.globals["settings"] = settings
# → 모든 템플릿에서 {{ settings.debug }} 등 사용 가능
```

### 7.3 템플릿에서 사용

```jinja2
{# 커스텀 필터 사용 #}
<p>작성일: {{ article.created_at | datetime }}</p>
{# 결과: 2024-01-15 14:30 #}

<p>작성일: {{ article.created_at | datetime('%Y년 %m월 %d일') }}</p>
{# 결과: 2024년 01월 15일 #}

<p>가격: {{ product.price | currency }}</p>
{# 결과: ₩1,500,000 #}

<p>{{ article.created_at | timeago }}</p>
{# 결과: 3시간 전 #}


{# 전역 변수 사용 #}
<title>{{ app_name }}</title>
{# 모든 페이지에서 앱 이름 사용 가능 #}

<footer>© {{ now().year }} {{ app_name }}</footer>
{# 결과: © 2024 앱이름 #}
```

---

## 8. 보안 고려사항

### 8.1 자동 이스케이프

Jinja2는 기본적으로 모든 변수를 **HTML 이스케이프**합니다.

```jinja2
{# ============================================================ #}
{# 자동 이스케이프 (기본 동작)                                   #}
{# ============================================================ #}

{# 사용자 입력 #}
{% set user_input = "<script>alert('해킹!')</script>" %}

{# 출력 #}
{{ user_input }}
{# 결과: &lt;script&gt;alert('해킹!')&lt;/script&gt; #}
{# → 스크립트가 실행되지 않고 텍스트로 표시됨 #}
{# → XSS 공격 방지! #}


{# ============================================================ #}
{# safe 필터 사용 시 주의                                        #}
{# ============================================================ #}

{# 위험한 사용 (절대 하지 마세요!) #}
{{ user_input | safe }}
{# 결과: <script>alert('해킹!')</script> #}
{# → 스크립트 실행됨! 보안 취약점! #}


{# ============================================================ #}
{# safe 필터의 올바른 사용                                       #}
{# ============================================================ #}

{# 1. 관리자가 작성한 신뢰할 수 있는 HTML #}
{{ admin_content | safe }}

{# 2. 서버에서 생성한 HTML #}
{{ render_markdown(article.content) | safe }}

{# 3. 신뢰할 수 있는 소스의 HTML #}
{{ trusted_widget_html | safe }}
```

### 8.2 안전한 사용 가이드

```jinja2
{# ============================================================ #}
{# 사용자 입력은 항상 자동 이스케이프 사용                       #}
{# ============================================================ #}

{# 좋은 예 #}
<p>작성자: {{ comment.author }}</p>
<p>내용: {{ comment.content }}</p>
{# → 악성 스크립트가 자동으로 무력화됨 #}


{# ============================================================ #}
{# URL도 주의해서 처리                                           #}
{# ============================================================ #}

{# 나쁜 예 #}
<a href="{{ user_provided_url }}">링크</a>
{# → javascript:alert('hack') 같은 URL이 들어올 수 있음! #}

{# 좋은 예 #}
{% if user_provided_url.startswith('https://') %}
<a href="{{ user_provided_url }}">링크</a>
{% endif %}


{# ============================================================ #}
{# 속성값에도 이스케이프 적용됨                                  #}
{# ============================================================ #}

<input value="{{ user_input }}">
{# user_input = '" onclick="alert(1)" data-x="' 이어도 안전 #}
{# 결과: <input value="&quot; onclick=&quot;alert(1)&quot; data-x=&quot;"> #}
```

---

## 9. 디버깅 팁

### 9.1 변수 내용 확인

```jinja2
{# ============================================================ #}
{# 디버그: 변수 타입과 내용 확인                                 #}
{# ============================================================ #}

<pre>{{ items | pprint }}</pre>
{#
   pprint: 변수 내용을 예쁘게 출력
   개발 중 데이터 구조 확인에 유용
#}


{# ============================================================ #}
{# 디버그: 사용 가능한 속성 확인                                 #}
{# ============================================================ #}

{% for attr in user.__dict__.keys() %}
<p>{{ attr }}: {{ user[attr] }}</p>
{% endfor %}
{# 객체의 모든 속성과 값을 출력 #}


{# ============================================================ #}
{# 조건부 디버그 출력                                            #}
{# ============================================================ #}

{% if settings.debug %}
<div class="debug-info">
    <p>현재 사용자: {{ current_user }}</p>
    <p>요청 URL: {{ request.url }}</p>
    <pre>{{ context | pprint }}</pre>
</div>
{% endif %}
{# settings.debug가 True일 때만 디버그 정보 표시 #}
```

---

## 10. 참고 자료

- [Jinja2 공식 문서](https://jinja.palletsprojects.com) - 가장 중요한 자료
- [Jinja2 템플릿 디자이너 문서](https://jinja.palletsprojects.com/en/3.1.x/templates/) - 템플릿 문법 상세 설명
- [FastAPI + Jinja2](https://fastapi.tiangolo.com/advanced/templates/) - FastAPI에서의 사용법

### 10.1 공부 순서 추천

1. 변수 출력 (`{{ }}`)과 제어문 (`{% %}`) 익히기
2. 조건문과 반복문 연습
3. 필터 사용법 익히기
4. 템플릿 상속 이해하기
5. 매크로 만들어보기
6. HTMX와 함께 파셜 템플릿 활용하기
