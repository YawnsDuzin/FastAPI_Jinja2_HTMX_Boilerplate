"""
Toasts Partials Router

토스트 알림 관련 HTMX 파셜 응답
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter()


@router.get("/success", response_class=HTMLResponse)
async def success_toast(request: Request, message: str = "성공적으로 처리되었습니다."):
    """성공 토스트"""
    return templates.TemplateResponse(
        request=request,
        name="partials/toasts/success.html",
        context={"message": message},
    )


@router.get("/error", response_class=HTMLResponse)
async def error_toast(request: Request, message: str = "오류가 발생했습니다."):
    """에러 토스트"""
    return templates.TemplateResponse(
        request=request,
        name="partials/toasts/error.html",
        context={"message": message},
    )


@router.get("/info", response_class=HTMLResponse)
async def info_toast(request: Request, message: str = "안내 메시지입니다."):
    """정보 토스트"""
    return templates.TemplateResponse(
        request=request,
        name="partials/toasts/info.html",
        context={"message": message},
    )


@router.get("/warning", response_class=HTMLResponse)
async def warning_toast(request: Request, message: str = "주의가 필요합니다."):
    """경고 토스트"""
    return templates.TemplateResponse(
        request=request,
        name="partials/toasts/warning.html",
        context={"message": message},
    )
