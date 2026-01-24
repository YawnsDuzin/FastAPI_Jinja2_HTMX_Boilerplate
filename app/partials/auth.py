"""
Auth Partials Router

인증 관련 HTMX 파셜 응답
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse

from app.api.deps import get_auth_service
from app.schemas.user import UserCreate
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_class=HTMLResponse)
async def register_partial(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    full_name: Optional[str] = Form(None),
):
    """회원가입 (HTMX)"""
    try:
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            full_name=full_name if full_name else None,
        )
        await auth_service.register(user_in)
        # auth_service가 사용하는 동일한 세션에서 commit
        await auth_service.db.commit()

        # 성공 - HX-Redirect로 로그인 페이지로 이동
        response = HTMLResponse(
            content="""
            <div class="p-4 bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-lg">
                회원가입이 완료되었습니다. 로그인 페이지로 이동합니다...
            </div>
            """,
            status_code=200,
        )
        response.headers["HX-Redirect"] = "/login"
        return response
    except Exception as e:
        await auth_service.db.rollback()
        error_message = str(e)
        if "이미 등록된 이메일" in error_message:
            error_message = "이미 등록된 이메일입니다."
        elif "이미 사용중인 사용자명" in error_message:
            error_message = "이미 사용 중인 사용자명입니다."

        return HTMLResponse(
            content=f"""
            <div class="p-4 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg">
                {error_message}
            </div>
            """,
            status_code=200,
        )


@router.post("/login", response_class=HTMLResponse)
async def login_partial(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    email: str = Form(...),
    password: str = Form(...),
):
    """로그인 (HTMX)"""
    try:
        tokens = await auth_service.login(email, password)

        # HTMLResponse 생성 후 쿠키와 헤더 설정
        response = HTMLResponse(content="", status_code=200)

        # 쿠키 설정
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=True,
            secure=False,  # Production에서는 True로 설정
            samesite="lax",
            max_age=3600,
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=604800,
        )

        # 성공 시 리다이렉트
        response.headers["HX-Redirect"] = "/dashboard"

        return response
    except Exception as e:
        error_message = str(e)
        if "올바르지 않습니다" in error_message:
            error_message = "이메일 또는 비밀번호가 올바르지 않습니다."

        return HTMLResponse(
            content=f"""
            <div class="p-4 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg">
                {error_message}
            </div>
            """,
            status_code=200,
        )
