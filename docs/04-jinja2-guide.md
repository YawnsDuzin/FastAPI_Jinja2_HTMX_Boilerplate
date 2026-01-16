# Jinja2 템플릿 가이드

## 1. Jinja2 소개

Jinja2는 Python용 현대적인 템플릿 엔진으로, HTML을 동적으로 생성하는 데 사용됩니다.

### 주요 특징
- 빠른 실행 속도 (컴파일된 템플릿)
- 자동 HTML 이스케이프 (XSS 방지)
- 템플릿 상속 지원
- 강력한 표현식 문법

## 2. 기본 문법

### 2.1 변수 출력

```jinja2
{# 변수 출력 #}
{{ username }}

{# 객체 속성 #}
{{ user.name }}
{{ user['email'] }}

{# 기본값 설정 #}
{{ username | default('Guest') }}

{# 필터 적용 #}
{{ title | upper }}
{{ content | truncate(100) }}
```

### 2.2 제어 구문

```jinja2
{# 조건문 #}
{% if user.is_authenticated %}
    <p>환영합니다, {{ user.name }}님!</p>
{% elif user.is_guest %}
    <p>게스트로 접속 중입니다.</p>
{% else %}
    <p>로그인해주세요.</p>
{% endif %}

{# 반복문 #}
{% for item in items %}
    <div class="item">
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
    </div>
{% else %}
    <p>아이템이 없습니다.</p>
{% endfor %}

{# 반복문 변수 #}
{% for item in items %}
    {{ loop.index }}      {# 1부터 시작하는 인덱스 #}
    {{ loop.index0 }}     {# 0부터 시작하는 인덱스 #}
    {{ loop.first }}      {# 첫 번째 항목인지 #}
    {{ loop.last }}       {# 마지막 항목인지 #}
    {{ loop.length }}     {# 전체 길이 #}
{% endfor %}
```

### 2.3 필터

```jinja2
{# 문자열 필터 #}
{{ "hello" | upper }}           {# HELLO #}
{{ "HELLO" | lower }}           {# hello #}
{{ "hello" | capitalize }}      {# Hello #}
{{ "hello" | title }}           {# Hello #}
{{ "  hello  " | trim }}        {# hello #}
{{ "hello" | replace("l", "x") }} {# hexxo #}

{# 숫자 필터 #}
{{ 3.14159 | round(2) }}        {# 3.14 #}
{{ 1234567 | format('{:,}') }}  {# 1,234,567 #}

{# 리스트 필터 #}
{{ items | length }}            {# 리스트 길이 #}
{{ items | first }}             {# 첫 번째 항목 #}
{{ items | last }}              {# 마지막 항목 #}
{{ items | join(', ') }}        {# 쉼표로 연결 #}
{{ items | sort }}              {# 정렬 #}
{{ items | reverse }}           {# 역순 #}

{# 날짜 필터 (커스텀) #}
{{ created_at | datetime }}
{{ created_at | date }}

{# 안전한 HTML 출력 #}
{{ html_content | safe }}
```

### 2.4 주석

```jinja2
{# 이것은 주석입니다. 렌더링되지 않습니다. #}

{#
    여러 줄
    주석도 가능합니다.
#}
```

## 3. 템플릿 상속

### 3.1 기본 템플릿 (base.html)

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}기본 제목{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    {% include "components/navbar.html" %}

    <main>
        {% block content %}{% endblock %}
    </main>

    {% include "components/footer.html" %}

    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### 3.2 자식 템플릿

```jinja2
{% extends "base.html" %}

{% block title %}페이지 제목{% endblock %}

{% block content %}
<div class="container">
    <h1>콘텐츠</h1>
    <p>페이지 내용</p>
</div>
{% endblock %}

{% block extra_scripts %}
<script src="/static/js/page.js"></script>
{% endblock %}
```

### 3.3 부모 블록 내용 포함

```jinja2
{% block content %}
{{ super() }}  {# 부모 블록 내용 포함 #}
<p>추가 내용</p>
{% endblock %}
```

## 4. 템플릿 포함과 매크로

### 4.1 Include

```jinja2
{# 단순 포함 #}
{% include "components/navbar.html" %}

{# 컨텍스트 전달 #}
{% include "components/item.html" with context %}

{# 없으면 무시 #}
{% include "components/optional.html" ignore missing %}
```

### 4.2 매크로 (재사용 가능한 함수)

```jinja2
{# macros.html #}
{% macro input(name, type='text', value='', label='') %}
<div class="form-group">
    {% if label %}
    <label for="{{ name }}">{{ label }}</label>
    {% endif %}
    <input type="{{ type }}"
           name="{{ name }}"
           id="{{ name }}"
           value="{{ value }}"
           class="form-control">
</div>
{% endmacro %}

{% macro button(text, type='submit', class='btn-primary') %}
<button type="{{ type }}" class="btn {{ class }}">
    {{ text }}
</button>
{% endmacro %}
```

```jinja2
{# 사용 #}
{% from "macros.html" import input, button %}

<form>
    {{ input('email', type='email', label='이메일') }}
    {{ input('password', type='password', label='비밀번호') }}
    {{ button('로그인') }}
</form>
```

## 5. 이 프로젝트의 템플릿 구조

### 5.1 디렉토리 구조

```
templates/
├── base.html                # 기본 레이아웃
├── components/              # 재사용 컴포넌트
│   ├── navbar.html
│   ├── footer.html
│   ├── sidebar.html
│   ├── modal.html
│   └── toast.html
├── pages/                   # 전체 페이지
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── items.html
└── partials/               # HTMX 파셜
    ├── items/
    │   ├── list.html
    │   ├── item.html
    │   ├── form.html
    │   └── empty.html
    ├── modals/
    │   ├── confirm.html
    │   └── alert.html
    └── toasts/
        ├── success.html
        ├── error.html
        └── info.html
```

### 5.2 base.html 구조

```jinja2
<!DOCTYPE html>
<html lang="ko" x-data="{ darkMode: false }">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{{ app_name }}{% endblock %}</title>

    {# CSS #}
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>

    {% block extra_head %}{% endblock %}
</head>
<body hx-boost="true">
    {# Toast Container #}
    <div id="toast-container"></div>

    {# Modal Container #}
    <div id="modal-container"></div>

    {# Navigation #}
    {% include "components/navbar.html" %}

    {# Main Content #}
    <main>
        {% block content %}{% endblock %}
    </main>

    {# Footer #}
    {% include "components/footer.html" %}

    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### 5.3 HTMX 파셜 예제

```jinja2
{# partials/items/item.html #}
<div id="item-{{ item.id }}" class="p-4 border rounded">
    <h3>{{ item.title }}</h3>
    {% if item.description %}
    <p>{{ item.description }}</p>
    {% endif %}
    <div class="flex gap-2">
        <button hx-get="/partials/items/{{ item.id }}/edit"
                hx-target="#modal-content"
                @click="$dispatch('openModal')">
            수정
        </button>
        <button hx-delete="/partials/items/{{ item.id }}"
                hx-target="#item-{{ item.id }}"
                hx-swap="outerHTML"
                hx-confirm="삭제하시겠습니까?">
            삭제
        </button>
    </div>
</div>
```

## 6. 커스텀 필터

### 6.1 프로젝트에서 정의된 필터

```python
# app/core/templates.py

def format_datetime(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)

def currency(value, symbol="₩"):
    return f"{symbol}{value:,.0f}"

# 등록
templates.env.filters["datetime"] = format_datetime
templates.env.filters["currency"] = currency
```

### 6.2 사용 예

```jinja2
{{ item.created_at | datetime }}
{{ item.created_at | datetime('%Y년 %m월 %d일') }}
{{ item.price | currency }}
```

## 7. 전역 변수

```python
# 전역 변수 등록
templates.env.globals["app_name"] = settings.app_name
templates.env.globals["now"] = datetime.now
```

```jinja2
{# 사용 #}
<footer>© {{ now().year }} {{ app_name }}</footer>
```

## 8. 보안 고려사항

### 8.1 자동 이스케이프
Jinja2는 기본적으로 모든 변수를 HTML 이스케이프합니다.

```jinja2
{# 안전 - 자동 이스케이프됨 #}
{{ user_input }}

{# 위험 - 이스케이프 비활성화 #}
{{ html_content | safe }}
```

### 8.2 안전한 사용

```jinja2
{# 사용자 입력은 항상 이스케이프 #}
{{ user.bio }}

{# 신뢰할 수 있는 마크다운만 safe 사용 #}
{{ markdown_to_html(trusted_content) | safe }}
```

## 9. 참고 자료

- [Jinja2 공식 문서](https://jinja.palletsprojects.com)
- [Jinja2 템플릿 디자이너 문서](https://jinja.palletsprojects.com/en/3.1.x/templates/)
