# SQLAlchemy 가이드

## 1. SQLAlchemy 소개

SQLAlchemy는 Python의 가장 강력한 ORM(Object-Relational Mapping) 라이브러리입니다. 이 프로젝트에서는 SQLAlchemy 2.0의 비동기 기능을 사용합니다.

### 주요 특징
- **ORM**: 객체 지향적 데이터베이스 작업
- **비동기 지원**: async/await 네이티브 지원
- **타입 힌트**: 완전한 타입 지원
- **다양한 데이터베이스**: SQLite, PostgreSQL, MySQL 등

## 2. 데이터베이스 설정

### 2.1 엔진 및 세션 설정

```python
# app/database.py
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

# 베이스 클래스
class Base(DeclarativeBase):
    pass

# 비동기 엔진
engine = create_async_engine(
    "sqlite+aiosqlite:///./app.db",
    echo=True,  # SQL 로깅
)

# 세션 팩토리
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 의존성 함수
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## 3. 모델 정의

### 3.1 기본 모델

```python
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
```

### 3.2 관계 정의

```python
from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.item import Item

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # 일대다 관계
    items: Mapped[List["Item"]] = relationship(
        "Item",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    # 외래 키
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    # 관계
    owner: Mapped["User"] = relationship("User", back_populates="items")
```

### 3.3 타입과 제약 조건

```python
from typing import Optional
from sqlalchemy import Boolean, Integer, Text, Numeric

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 필수 필드
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # 선택적 필드
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 기본값
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    # 소수점
    price: Mapped[float] = mapped_column(Numeric(10, 2))
```

## 4. CRUD 작업

### 4.1 생성 (Create)

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(db: AsyncSession, email: str, username: str) -> User:
    user = User(email=email, username=username)
    db.add(user)
    await db.flush()  # ID 생성
    await db.refresh(user)  # 새로고침
    return user
```

### 4.2 조회 (Read)

```python
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# 단일 조회
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# 조건 조회
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

# 목록 조회
async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> list[User]:
    result = await db.execute(
        select(User)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())

# 관계 로드 (Eager Loading)
async def get_user_with_items(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(
        select(User)
        .options(joinedload(User.items))
        .where(User.id == user_id)
    )
    return result.unique().scalar_one_or_none()
```

### 4.3 수정 (Update)

```python
async def update_user(
    db: AsyncSession,
    user: User,
    email: Optional[str] = None,
    username: Optional[str] = None
) -> User:
    if email:
        user.email = email
    if username:
        user.username = username

    await db.flush()
    await db.refresh(user)
    return user
```

### 4.4 삭제 (Delete)

```python
async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.flush()
```

## 5. 쿼리 빌더

### 5.1 필터링

```python
from sqlalchemy import select, and_, or_

# 단순 필터
query = select(User).where(User.is_active == True)

# 여러 조건 (AND)
query = select(User).where(
    and_(
        User.is_active == True,
        User.is_verified == True
    )
)

# OR 조건
query = select(User).where(
    or_(
        User.email.like("%@example.com"),
        User.is_superuser == True
    )
)

# IN 조건
query = select(User).where(User.id.in_([1, 2, 3]))

# LIKE 검색
query = select(Item).where(Item.title.ilike(f"%{search}%"))

# NULL 체크
query = select(User).where(User.deleted_at.is_(None))
```

### 5.2 정렬과 페이징

```python
from sqlalchemy import desc, asc

# 정렬
query = select(Item).order_by(Item.created_at.desc())

# 여러 필드 정렬
query = select(Item).order_by(
    Item.priority.desc(),
    Item.created_at.desc()
)

# 페이징
query = select(Item).offset(10).limit(20)
```

### 5.3 집계 함수

```python
from sqlalchemy import func

# 개수
async def count_items(db: AsyncSession, owner_id: int) -> int:
    result = await db.execute(
        select(func.count(Item.id))
        .where(Item.owner_id == owner_id)
    )
    return result.scalar() or 0

# 합계, 평균
query = select(
    func.sum(Order.total),
    func.avg(Order.total)
).where(Order.user_id == user_id)
```

## 6. 마이그레이션 (Alembic)

### 6.1 기본 명령어

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Add users table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1

# 현재 버전 확인
alembic current

# 히스토리 확인
alembic history
```

### 6.2 마이그레이션 파일 예시

```python
# alembic/versions/xxxx_add_users_table.py

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_users_email', 'users', ['email'])


def downgrade() -> None:
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

## 7. 트랜잭션

### 7.1 자동 커밋/롤백

```python
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 7.2 명시적 트랜잭션

```python
async def transfer_money(
    db: AsyncSession,
    from_id: int,
    to_id: int,
    amount: float
):
    async with db.begin():
        from_account = await get_account(db, from_id)
        to_account = await get_account(db, to_id)

        from_account.balance -= amount
        to_account.balance += amount
        # 자동 커밋
```

## 8. 성능 최적화

### 8.1 인덱스

```python
class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), index=True)

    __table_args__ = (
        Index('ix_user_search', 'username', 'email'),
    )
```

### 8.2 Eager Loading

```python
# joinedload: JOIN으로 한 번에 로드
query = select(User).options(joinedload(User.items))

# selectinload: 별도 쿼리로 로드
query = select(User).options(selectinload(User.items))
```

### 8.3 벌크 작업

```python
# 벌크 삽입
items = [Item(title=f"Item {i}") for i in range(1000)]
db.add_all(items)
await db.flush()

# 벌크 업데이트
await db.execute(
    update(Item)
    .where(Item.is_active == False)
    .values(deleted_at=datetime.now())
)
```

## 9. 참고 자료

- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy 비동기 가이드](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic 문서](https://alembic.sqlalchemy.org/en/latest/)
