"""
API v1 Router

모든 v1 API 라우터 통합
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.items import router as items_router
from app.api.v1.users import router as users_router

api_router = APIRouter()

# 라우터 등록
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(items_router, prefix="/items", tags=["items"])
