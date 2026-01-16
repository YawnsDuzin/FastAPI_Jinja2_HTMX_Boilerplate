"""
Custom Exception Handlers

커스텀 예외 클래스와 전역 예외 핸들러 정의
"""

import json
from typing import Any, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.config import settings


class AppException(Exception):
    """
    애플리케이션 기본 예외 클래스

    모든 커스텀 예외는 이 클래스를 상속받습니다.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        detail: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class AuthenticationError(AppException):
    """인증 실패 예외"""

    def __init__(self, message: str = "인증에 실패했습니다."):
        super().__init__(message=message, status_code=401)


class AuthorizationError(AppException):
    """권한 부족 예외"""

    def __init__(self, message: str = "권한이 없습니다."):
        super().__init__(message=message, status_code=403)


class NotFoundError(AppException):
    """리소스 미발견 예외"""

    def __init__(self, message: str = "요청한 리소스를 찾을 수 없습니다."):
        super().__init__(message=message, status_code=404)


class ValidationError(AppException):
    """유효성 검사 실패 예외"""

    def __init__(
        self, message: str = "입력값이 유효하지 않습니다.", detail: Optional[dict] = None
    ):
        super().__init__(message=message, status_code=422, detail=detail)


class ConflictError(AppException):
    """리소스 충돌 예외"""

    def __init__(self, message: str = "리소스 충돌이 발생했습니다."):
        super().__init__(message=message, status_code=409)


def is_htmx_request(request: Request) -> bool:
    """HTMX 요청 여부 확인"""
    return request.headers.get("HX-Request") == "true"


def setup_exception_handlers(app: FastAPI) -> None:
    """전역 예외 핸들러 설정"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """AppException 핸들러"""
        if is_htmx_request(request):
            # HTMX 요청인 경우 토스트 메시지 반환
            response = HTMLResponse(
                content=f"""
                <div class="toast toast-error"
                     x-data="{{show: true}}"
                     x-show="show"
                     x-init="setTimeout(() => show = false, 5000)">
                    <div class="alert alert-error">
                        <span>{exc.message}</span>
                    </div>
                </div>
                """,
                status_code=exc.status_code,
            )
            response.headers["HX-Retarget"] = "#toast-container"
            response.headers["HX-Reswap"] = "beforeend"
            return response

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        """404 에러 핸들러"""
        if is_htmx_request(request):
            return HTMLResponse(
                content="<div class='text-error'>페이지를 찾을 수 없습니다.</div>",
                status_code=404,
            )

        # API 요청인 경우
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=404,
                content={"error": True, "message": "리소스를 찾을 수 없습니다."},
            )

        # 페이지 요청인 경우 404 페이지 렌더링
        from app.core.templates import templates

        return templates.TemplateResponse(
            request=request,
            name="pages/404.html",
            status_code=404,
        )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        """500 에러 핸들러"""
        if settings.debug:
            import traceback

            error_detail = traceback.format_exc()
        else:
            error_detail = "서버 내부 오류가 발생했습니다."

        if is_htmx_request(request):
            return HTMLResponse(
                content=f"""
                <div class="toast toast-error">
                    <div class="alert alert-error">
                        <span>서버 오류가 발생했습니다.</span>
                    </div>
                </div>
                """,
                status_code=500,
            )

        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=500,
                content={
                    "error": True,
                    "message": "서버 내부 오류가 발생했습니다.",
                    "detail": error_detail if settings.debug else None,
                },
            )

        from app.core.templates import templates

        return templates.TemplateResponse(
            request=request,
            name="pages/500.html",
            context={"error_detail": error_detail if settings.debug else None},
            status_code=500,
        )
