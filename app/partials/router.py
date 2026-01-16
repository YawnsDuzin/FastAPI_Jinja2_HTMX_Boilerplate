"""
Partials Router

모든 파셜 라우터 통합
"""

from fastapi import APIRouter

from app.partials.items import router as items_router
from app.partials.modals import router as modals_router
from app.partials.toasts import router as toasts_router

partials_router = APIRouter()

# 라우터 등록
partials_router.include_router(items_router, prefix="/items", tags=["partials"])
partials_router.include_router(modals_router, prefix="/modals", tags=["partials"])
partials_router.include_router(toasts_router, prefix="/toasts", tags=["partials"])
