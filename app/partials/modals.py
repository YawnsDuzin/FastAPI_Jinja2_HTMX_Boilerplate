"""
Modals Partials Router

모달 관련 HTMX 파셜 응답
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.deps import CurrentUser
from app.core.templates import templates

router = APIRouter()


@router.get("/confirm", response_class=HTMLResponse)
async def confirm_modal(
    request: Request,
    current_user: CurrentUser,
    title: str = "확인",
    message: str = "정말 진행하시겠습니까?",
    confirm_url: str = "",
    confirm_method: str = "DELETE",
    confirm_target: str = "",
):
    """
    확인 모달 파셜

    범용 확인 대화상자 모달

    Args:
        title: 모달 제목
        message: 확인 메시지
        confirm_url: 확인 시 호출할 URL
        confirm_method: HTTP 메서드
        confirm_target: HX-target
    """
    return templates.TemplateResponse(
        request=request,
        name="partials/modals/confirm.html",
        context={
            "title": title,
            "message": message,
            "confirm_url": confirm_url,
            "confirm_method": confirm_method,
            "confirm_target": confirm_target,
        },
    )


@router.get("/alert", response_class=HTMLResponse)
async def alert_modal(
    request: Request,
    title: str = "알림",
    message: str = "",
    type: str = "info",
):
    """
    알림 모달 파셜

    단순 알림 메시지 모달

    Args:
        title: 모달 제목
        message: 알림 메시지
        type: 알림 타입 (info, success, warning, error)
    """
    return templates.TemplateResponse(
        request=request,
        name="partials/modals/alert.html",
        context={
            "title": title,
            "message": message,
            "type": type,
        },
    )


@router.get("/form/{form_type}", response_class=HTMLResponse)
async def form_modal(
    request: Request,
    current_user: CurrentUser,
    form_type: str,
    item_id: int = None,
):
    """
    폼 모달 파셜

    다양한 폼을 모달로 표시

    Args:
        form_type: 폼 타입 (item-create, item-edit, etc.)
        item_id: 수정할 아이템 ID
    """
    context = {
        "form_type": form_type,
        "item_id": item_id,
    }

    return templates.TemplateResponse(
        request=request,
        name="partials/modals/form.html",
        context=context,
    )
