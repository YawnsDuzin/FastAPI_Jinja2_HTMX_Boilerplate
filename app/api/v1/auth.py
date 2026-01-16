"""
Auth API Endpoints

인증 관련 API 엔드포인트
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.api.deps import (
    CurrentUser,
    DbSession,
    get_auth_service,
)
from app.schemas.user import Token, User, UserCreate, UserLogin
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    회원가입

    - **email**: 이메일 (유일해야 함)
    - **username**: 사용자명 (유일해야 함)
    - **password**: 비밀번호 (8자 이상)
    - **full_name**: 이름 (선택)
    """
    user = await auth_service.register(user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    user_in: UserLogin,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    로그인

    인증 성공 시 JWT 토큰을 쿠키에 설정하고 반환합니다.
    """
    tokens = await auth_service.login(user_in.email, user_in.password)

    # 쿠키 설정 (httpOnly, secure)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False,  # Production에서는 True로 설정
        samesite="lax",
        max_age=3600,  # 1시간
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800,  # 7일
    )

    return tokens


@router.post("/logout")
async def logout(response: Response):
    """
    로그아웃

    쿠키에서 토큰을 제거합니다.
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "로그아웃되었습니다."}


@router.post("/refresh", response_model=Token)
async def refresh_tokens(
    response: Response,
    refresh_token: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    토큰 갱신

    리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급합니다.
    """
    tokens = await auth_service.refresh_tokens(refresh_token)

    # 새 토큰으로 쿠키 갱신
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False,
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

    return tokens


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: CurrentUser):
    """
    현재 사용자 정보

    인증된 사용자의 프로필 정보를 반환합니다.
    """
    return current_user
