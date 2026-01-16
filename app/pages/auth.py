"""
Auth Page Router

인증 관련 페이지 렌더링 (로그인, 회원가입)
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.deps import CurrentUserOptional
from app.core.templates import templates

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, current_user: CurrentUserOptional):
    """로그인 페이지"""
    # 이미 로그인된 경우 대시보드로 리다이렉트
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="pages/login.html",
        context={
            "title": "로그인",
            "current_user": current_user,
        },
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, current_user: CurrentUserOptional):
    """회원가입 페이지"""
    # 이미 로그인된 경우 대시보드로 리다이렉트
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="pages/register.html",
        context={
            "title": "회원가입",
            "current_user": current_user,
        },
    )


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request, current_user: CurrentUserOptional):
    """비밀번호 찾기 페이지"""
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="pages/forgot-password.html",
        context={
            "title": "비밀번호 찾기",
            "current_user": current_user,
        },
    )
