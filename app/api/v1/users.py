"""
Users API Endpoints

사용자 관리 API 엔드포인트
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    CurrentSuperuser,
    CurrentUser,
    DbSession,
    get_user_service,
)
from app.schemas.user import PasswordChange, User, UserUpdate
from app.services.auth import AuthService
from app.services.user import UserService

router = APIRouter()


@router.get("", response_model=List[User])
async def get_users(
    current_user: CurrentSuperuser,
    user_service: Annotated[UserService, Depends(get_user_service)],
    skip: int = 0,
    limit: int = 100,
):
    """
    사용자 목록 조회 (관리자 전용)
    """
    users = await user_service.get_all(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    current_user: CurrentUser,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    특정 사용자 조회

    자신의 정보이거나 관리자만 조회 가능
    """
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )

    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )
    return user


@router.patch("/me", response_model=User)
async def update_current_user(
    user_in: UserUpdate,
    current_user: CurrentUser,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    현재 사용자 정보 수정
    """
    # 이메일 중복 확인
    if user_in.email:
        if await user_service.is_email_taken(user_in.email, current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용중인 이메일입니다.",
            )

    # 사용자명 중복 확인
    if user_in.username:
        if await user_service.is_username_taken(user_in.username, current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용중인 사용자명입니다.",
            )

    user = await user_service.update(current_user, user_in)
    return user


@router.post("/me/change-password")
async def change_password(
    db: DbSession,
    password_in: PasswordChange,
    current_user: CurrentUser,
):
    """
    비밀번호 변경
    """
    auth_service = AuthService(db)
    await auth_service.change_password(
        current_user,
        password_in.current_password,
        password_in.new_password,
    )
    return {"message": "비밀번호가 변경되었습니다."}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: CurrentSuperuser,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    사용자 삭제 (관리자 전용)
    """
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자기 자신은 삭제할 수 없습니다.",
        )

    await user_service.delete(user)
    return {"message": "사용자가 삭제되었습니다."}
