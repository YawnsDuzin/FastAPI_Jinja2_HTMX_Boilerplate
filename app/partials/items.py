"""
Items Partials Router

아이템 관련 HTMX 파셜 응답
"""

import json
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse

from app.api.deps import CurrentUser, get_item_service
from app.core.templates import templates
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item import ItemService

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def get_items_partial(
    request: Request,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
):
    """아이템 목록 파셜"""
    page_size = 10
    skip = (page - 1) * page_size

    items = await item_service.get_all(
        owner_id=current_user.id,
        skip=skip,
        limit=page_size,
        search=search,
    )

    return templates.TemplateResponse(
        request=request,
        name="partials/items/list.html",
        context={"items": items, "search": search},
    )


@router.get("/form", response_class=HTMLResponse)
async def get_item_form(request: Request, current_user: CurrentUser):
    """아이템 생성 폼 파셜"""
    return templates.TemplateResponse(
        request=request,
        name="partials/items/form.html",
        context={"item": None, "action": "create"},
    )


@router.get("/{item_id}", response_class=HTMLResponse)
async def get_item_partial(
    request: Request,
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """단일 아이템 파셜"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="partials/items/item.html",
        context={"item": item},
    )


@router.get("/{item_id}/edit", response_class=HTMLResponse)
async def get_item_edit_form(
    request: Request,
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 수정 폼 파셜"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="partials/items/form.html",
        context={"item": item, "action": "edit"},
    )


@router.post("", response_class=HTMLResponse)
async def create_item_partial(
    request: Request,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    title: str = Form(...),
    description: Optional[str] = Form(None),
    priority: int = Form(0),
):
    """아이템 생성 (HTMX)"""
    item_in = ItemCreate(title=title, description=description, priority=priority)
    item = await item_service.create(item_in, current_user)

    response = templates.TemplateResponse(
        request=request,
        name="partials/items/item.html",
        context={"item": item},
    )

    # 토스트 알림 트리거
    response.headers["HX-Trigger"] = json.dumps(
        {
            "showToast": {"type": "success", "message": "아이템이 생성되었습니다."},
            "closeModal": True,
        }
    )

    return response


@router.put("/{item_id}", response_class=HTMLResponse)
async def update_item_partial(
    request: Request,
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    title: str = Form(...),
    description: Optional[str] = Form(None),
    priority: int = Form(0),
):
    """아이템 수정 (HTMX)"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    item_in = ItemUpdate(title=title, description=description, priority=priority)
    updated_item = await item_service.update(item, item_in)

    response = templates.TemplateResponse(
        request=request,
        name="partials/items/item.html",
        context={"item": updated_item},
    )

    response.headers["HX-Trigger"] = json.dumps(
        {
            "showToast": {"type": "success", "message": "아이템이 수정되었습니다."},
            "closeModal": True,
        }
    )

    return response


@router.delete("/{item_id}", response_class=HTMLResponse)
async def delete_item_partial(
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 삭제 (HTMX)"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    await item_service.delete(item)

    response = HTMLResponse(content="")
    response.headers["HX-Trigger"] = json.dumps(
        {"showToast": {"type": "success", "message": "아이템이 삭제되었습니다."}}
    )

    return response


@router.post("/{item_id}/toggle", response_class=HTMLResponse)
async def toggle_item_partial(
    request: Request,
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """아이템 활성/비활성 토글 (HTMX)"""
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    updated_item = await item_service.toggle_active(item)

    response = templates.TemplateResponse(
        request=request,
        name="partials/items/item.html",
        context={"item": updated_item},
    )

    status = "활성화" if updated_item.is_active else "비활성화"
    response.headers["HX-Trigger"] = json.dumps(
        {"showToast": {"type": "info", "message": f"아이템이 {status}되었습니다."}}
    )

    return response
