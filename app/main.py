"""
FastAPI Application Entry Point

애플리케이션 초기화, 미들웨어 설정, 라우터 등록을 담당합니다.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.templates import templates
from app.database import close_db, init_db
from app.pages.router import pages_router
from app.partials.router import partials_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    애플리케이션 수명주기 관리

    시작 시 데이터베이스 초기화, 종료 시 연결 정리
    """
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 팩토리"""
    app = FastAPI(
        title=settings.app_name,
        description="FastAPI + Jinja2 + HTMX Boilerplate",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # CORS 미들웨어
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 정적 파일 마운트
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # 예외 핸들러 설정
    setup_exception_handlers(app)

    # API 라우터 등록
    app.include_router(api_router, prefix="/api/v1")

    # 페이지 라우터 등록
    app.include_router(pages_router)

    # 파셜 라우터 등록
    app.include_router(partials_router, prefix="/partials")

    return app


app = create_app()


@app.get("/health", tags=["health"])
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "app": settings.app_name}
