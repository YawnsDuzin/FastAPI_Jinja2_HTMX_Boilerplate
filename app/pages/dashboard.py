"""
Dashboard Page Router

대시보드 및 인증이 필요한 페이지 렌더링
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.deps import CurrentUser, DbSession, get_item_service
from app.core.templates import templates
from app.services.item import ItemService

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """대시보드 메인"""
    # 최근 아이템 조회
    recent_items = await item_service.get_all(
        owner_id=current_user.id,
        limit=5,
    )

    # 통계
    total_items = await item_service.count(owner_id=current_user.id)
    active_items = await item_service.count(owner_id=current_user.id, is_active=True)

    return templates.TemplateResponse(
        request=request,
        name="pages/dashboard.html",
        context={
            "title": "대시보드",
            "current_user": current_user,
            "recent_items": recent_items,
            "stats": {
                "total_items": total_items,
                "active_items": active_items,
            },
        },
    )


@router.get("/items", response_class=HTMLResponse)
async def items_page(
    request: Request,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    page: int = Query(1, ge=1),
    search: Optional[str] = None,
):
    """아이템 목록 페이지"""
    page_size = 10
    skip = (page - 1) * page_size

    items = await item_service.get_all(
        owner_id=current_user.id,
        skip=skip,
        limit=page_size,
        search=search,
    )
    total = await item_service.count(owner_id=current_user.id, search=search)
    total_pages = (total + page_size - 1) // page_size

    return templates.TemplateResponse(
        request=request,
        name="pages/items.html",
        context={
            "title": "아이템 관리",
            "current_user": current_user,
            "items": items,
            "page": page,
            "total_pages": total_pages,
            "total": total,
            "search": search,
        },
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, current_user: CurrentUser):
    """프로필 페이지"""
    return templates.TemplateResponse(
        request=request,
        name="pages/profile.html",
        context={
            "title": "프로필",
            "current_user": current_user,
        },
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, current_user: CurrentUser):
    """설정 페이지"""
    return templates.TemplateResponse(
        request=request,
        name="pages/settings.html",
        context={
            "title": "설정",
            "current_user": current_user,
        },
    )
