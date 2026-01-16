"""
Home Page Router

홈페이지 렌더링
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.deps import CurrentUserOptional
from app.core.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: CurrentUserOptional):
    """홈페이지"""
    return templates.TemplateResponse(
        request=request,
        name="pages/home.html",
        context={
            "title": "홈",
            "current_user": current_user,
        },
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, current_user: CurrentUserOptional):
    """소개 페이지"""
    return templates.TemplateResponse(
        request=request,
        name="pages/about.html",
        context={
            "title": "소개",
            "current_user": current_user,
        },
    )
