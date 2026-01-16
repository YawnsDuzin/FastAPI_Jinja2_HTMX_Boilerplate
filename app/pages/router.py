"""
Pages Router

모든 페이지 라우터 통합
"""

from fastapi import APIRouter

from app.pages.auth import router as auth_router
from app.pages.dashboard import router as dashboard_router
from app.pages.home import router as home_router

pages_router = APIRouter()

# 라우터 등록
pages_router.include_router(home_router, tags=["pages"])
pages_router.include_router(auth_router, tags=["pages"])
pages_router.include_router(dashboard_router, tags=["pages"])
