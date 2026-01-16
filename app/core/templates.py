"""
Jinja2 Template Configuration

템플릿 엔진 설정 및 커스텀 필터/함수 정의
"""

from datetime import datetime
from typing import Any

from fastapi.templating import Jinja2Templates

from app.config import settings

# Jinja2 템플릿 인스턴스 생성
templates = Jinja2Templates(directory="templates")


def format_datetime(value: datetime, format: str = "%Y-%m-%d %H:%M") -> str:
    """날짜/시간 포맷팅 필터"""
    if value is None:
        return ""
    return value.strftime(format)


def format_date(value: datetime, format: str = "%Y-%m-%d") -> str:
    """날짜 포맷팅 필터"""
    if value is None:
        return ""
    return value.strftime(format)


def truncate(value: str, length: int = 100, suffix: str = "...") -> str:
    """문자열 자르기 필터"""
    if value is None:
        return ""
    if len(value) <= length:
        return value
    return value[:length].rsplit(" ", 1)[0] + suffix


def currency(value: float, symbol: str = "₩") -> str:
    """통화 포맷팅 필터"""
    if value is None:
        return f"{symbol}0"
    return f"{symbol}{value:,.0f}"


def nl2br(value: str) -> str:
    """줄바꿈을 <br> 태그로 변환"""
    if value is None:
        return ""
    return value.replace("\n", "<br>")


# 커스텀 필터 등록
templates.env.filters["datetime"] = format_datetime
templates.env.filters["date"] = format_date
templates.env.filters["truncate"] = truncate
templates.env.filters["currency"] = currency
templates.env.filters["nl2br"] = nl2br


# 전역 컨텍스트 변수
templates.env.globals["app_name"] = settings.app_name
templates.env.globals["debug"] = settings.debug
templates.env.globals["now"] = datetime.now


def render_template(name: str, context: dict[str, Any] = None) -> str:
    """
    템플릿을 문자열로 렌더링

    HTMX 응답이나 이메일 템플릿 등에 사용

    Args:
        name: 템플릿 파일 이름
        context: 템플릿 컨텍스트

    Returns:
        렌더링된 HTML 문자열
    """
    if context is None:
        context = {}
    template = templates.env.get_template(name)
    return template.render(**context)
