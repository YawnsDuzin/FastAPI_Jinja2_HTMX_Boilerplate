"""
Items API Endpoints

아이템 CRUD API 엔드포인트
"""

from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import (
    CurrentUser,
    get_item_service,
)
from app.schemas.common import PaginatedResponse
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item import ItemService

router = APIRouter()


@router.get("", response_model=List[Item])
async def get_items(
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    """
    아이템 목록 조회

    현재 사용자의 아이템만 조회됩니다.
    """
    items = await item_service.get_all(
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
    )
    return items


@router.get("/paginated", response_model=PaginatedResponse[Item])
async def get_items_paginated(
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    """
    아이템 목록 조회 (페이지네이션)
    """
    skip = (page - 1) * size
    items = await item_service.get_all(
        owner_id=current_user.id,
        skip=skip,
        limit=size,
        search=search,
        is_active=is_active,
    )
    total = await item_service.count(
        owner_id=current_user.id,
        search=search,
        is_active=is_active,
    )

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=page,
        size=size,
    )


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """
    아이템 상세 조회
    """
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    return item


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """
    아이템 생성
    """
    item = await item_service.create(item_in, current_user)
    return item


@router.patch("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """
    아이템 수정
    """
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    updated_item = await item_service.update(item, item_in)
    return updated_item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """
    아이템 삭제
    """
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    await item_service.delete(item)
    return {"message": "아이템이 삭제되었습니다."}


@router.post("/{item_id}/toggle", response_model=Item)
async def toggle_item_active(
    item_id: int,
    current_user: CurrentUser,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    """
    아이템 활성/비활성 토글
    """
    item = await item_service.get_or_404(item_id, owner_id=current_user.id)
    updated_item = await item_service.toggle_active(item)
    return updated_item
