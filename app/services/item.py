"""
Item Service

아이템 관련 비즈니스 로직
"""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.exceptions import NotFoundError
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """아이템 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        item_id: int,
        owner_id: Optional[int] = None,
    ) -> Optional[Item]:
        """
        ID로 아이템 조회

        Args:
            item_id: 아이템 ID
            owner_id: 소유자 ID (지정 시 소유자 검증)
        """
        query = select(Item).where(Item.id == item_id)
        if owner_id:
            query = query.where(Item.owner_id == owner_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_with_owner(self, item_id: int) -> Optional[Item]:
        """소유자 정보 포함 아이템 조회"""
        query = (
            select(Item)
            .options(joinedload(Item.owner))
            .where(Item.id == item_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> list[Item]:
        """아이템 목록 조회"""
        query = select(Item)

        if owner_id:
            query = query.where(Item.owner_id == owner_id)

        if is_active is not None:
            query = query.where(Item.is_active == is_active)

        if search:
            query = query.where(
                Item.title.ilike(f"%{search}%")
                | Item.description.ilike(f"%{search}%")
            )

        query = query.order_by(Item.priority.desc(), Item.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(
        self,
        owner_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> int:
        """아이템 개수 조회"""
        query = select(func.count(Item.id))

        if owner_id:
            query = query.where(Item.owner_id == owner_id)

        if is_active is not None:
            query = query.where(Item.is_active == is_active)

        if search:
            query = query.where(
                Item.title.ilike(f"%{search}%")
                | Item.description.ilike(f"%{search}%")
            )

        result = await self.db.execute(query)
        return result.scalar() or 0

    async def create(self, item_in: ItemCreate, owner: User) -> Item:
        """아이템 생성"""
        item = Item(
            title=item_in.title,
            description=item_in.description,
            priority=item_in.priority,
            owner_id=owner.id,
        )
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, item_in: ItemUpdate) -> Item:
        """아이템 수정"""
        update_data = item_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        """아이템 삭제"""
        await self.db.delete(item)
        await self.db.flush()

    async def toggle_active(self, item: Item) -> Item:
        """아이템 활성/비활성 토글"""
        item.is_active = not item.is_active
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def get_or_404(
        self,
        item_id: int,
        owner_id: Optional[int] = None,
    ) -> Item:
        """
        아이템 조회 (없으면 404 에러)

        Args:
            item_id: 아이템 ID
            owner_id: 소유자 ID

        Returns:
            아이템

        Raises:
            NotFoundError: 아이템을 찾을 수 없음
        """
        item = await self.get_by_id(item_id, owner_id)
        if not item:
            raise NotFoundError("아이템을 찾을 수 없습니다.")
        return item
