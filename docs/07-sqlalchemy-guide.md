# SQLAlchemy 가이드

## 1. SQLAlchemy란?

### 1.1 SQLAlchemy 소개

SQLAlchemy는 Python에서 데이터베이스를 다루는 **ORM(Object-Relational Mapping)** 라이브러리입니다.

```
ORM이란?
- Object: Python 객체 (클래스)
- Relational: 관계형 데이터베이스 (테이블)
- Mapping: 연결

즉, Python 클래스를 데이터베이스 테이블과 연결해주는 기술입니다.
```

### 1.2 왜 ORM을 사용하나요?

**SQL 직접 작성 방식:**
```python
# 순수 SQL 쿼리 (위험하고 불편함)
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 사용자 조회
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
row = cursor.fetchone()

# 딕셔너리로 변환해야 사용 가능
user = {
    'id': row[0],
    'email': row[1],
    'username': row[2]
}
```

**SQLAlchemy ORM 방식:**
```python
# SQLAlchemy ORM (안전하고 편리함)
from sqlalchemy import select

# 사용자 조회 - Python 객체로 바로 사용 가능!
result = await db.execute(select(User).where(User.id == user_id))
user = result.scalar_one_or_none()

# user.id, user.email, user.username 바로 접근 가능
print(user.email)
```

### 1.3 ORM의 장점

| 장점 | 설명 |
|------|------|
| SQL 인젝션 방지 | 자동으로 파라미터 이스케이프 |
| 타입 안전성 | Python 타입 힌트 지원 |
| 코드 재사용 | 모델 클래스로 일관된 구조 |
| 데이터베이스 독립성 | SQLite → PostgreSQL 쉽게 전환 |
| 관계 처리 | 테이블 간 관계를 Python 객체로 표현 |

### 1.4 SQLAlchemy 2.0

이 프로젝트는 **SQLAlchemy 2.0**을 사용합니다.

```
SQLAlchemy 1.x vs 2.0 차이점:
- 2.0: 비동기(async/await) 지원
- 2.0: 더 강력한 타입 힌트
- 2.0: select() 함수 기반 쿼리
```

---

## 2. 프로젝트 구조

### 2.1 데이터베이스 관련 파일

```
app/
├── database.py          # 데이터베이스 연결 설정
├── models/
│   ├── __init__.py      # 모델 export
│   ├── base.py          # Base 클래스 정의
│   ├── user.py          # User 모델
│   └── item.py          # Item 모델
└── services/
    ├── user_service.py  # User CRUD 로직
    └── item_service.py  # Item CRUD 로직
```

---

## 3. 데이터베이스 설정

### 3.1 연결 설정 (database.py)

```python
# app/database.py

from sqlalchemy.ext.asyncio import (
    AsyncSession,          # 비동기 세션 클래스
    async_sessionmaker,    # 세션 팩토리 생성 함수
    create_async_engine,   # 비동기 엔진 생성 함수
)
from sqlalchemy.orm import DeclarativeBase

# ============================================================
# 1. 베이스 클래스 정의
# ============================================================
class Base(DeclarativeBase):
    """
    모든 모델 클래스가 상속받는 베이스 클래스

    DeclarativeBase를 상속받아 SQLAlchemy가 이 클래스를
    상속받는 모든 클래스를 테이블로 인식합니다.
    """
    pass
# DeclarativeBase: SQLAlchemy 2.0의 새로운 베이스 클래스
# 이전 버전의 declarative_base() 함수를 대체


# ============================================================
# 2. 데이터베이스 엔진 생성
# ============================================================
DATABASE_URL = "sqlite+aiosqlite:///./app.db"
# 데이터베이스 URL 형식:
# dialect+driver://username:password@host:port/database
#
# sqlite+aiosqlite: SQLite 데이터베이스 + 비동기 드라이버
# :///./app.db: 현재 폴더의 app.db 파일 사용
#
# 다른 예시:
# PostgreSQL: "postgresql+asyncpg://user:pass@localhost:5432/dbname"
# MySQL: "mysql+aiomysql://user:pass@localhost:3306/dbname"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL 쿼리 로깅 (개발 시 유용, 운영에서는 False)
)
# create_async_engine: 비동기 데이터베이스 엔진 생성
# engine: 데이터베이스 연결 풀을 관리하는 객체
# echo=True: 실행되는 모든 SQL을 콘솔에 출력


# ============================================================
# 3. 세션 팩토리 생성
# ============================================================
async_session_maker = async_sessionmaker(
    engine,                    # 사용할 엔진
    class_=AsyncSession,       # 세션 클래스 (비동기)
    expire_on_commit=False,    # 커밋 후에도 객체 속성 접근 가능
)
# async_sessionmaker: 세션 객체를 생성하는 팩토리
# class_=AsyncSession: 비동기 세션 사용
# expire_on_commit=False:
#   - True (기본값): 커밋 후 객체 접근 시 DB 다시 조회
#   - False: 커밋 후에도 메모리의 값 사용 가능


# ============================================================
# 4. 의존성 함수 (FastAPI에서 사용)
# ============================================================
async def get_db():
    """
    FastAPI 의존성으로 사용되는 데이터베이스 세션 제공 함수

    사용 예시:
    @router.get("/users")
    async def get_users(db: AsyncSession = Depends(get_db)):
        ...
    """
    async with async_session_maker() as session:
        # async with: 비동기 컨텍스트 매니저
        # async_session_maker(): 새 세션 생성
        # session: 데이터베이스 세션 객체

        try:
            yield session
            # yield: FastAPI에 세션 제공
            # 라우터 함수가 끝나면 아래 코드 실행

            await session.commit()
            # 모든 변경사항 커밋 (저장)

        except Exception:
            await session.rollback()
            # 예외 발생 시 롤백 (변경사항 취소)
            raise
            # 예외를 다시 발생시켜 FastAPI가 처리하도록
```

### 3.2 세션의 생명주기

```
요청 시작
    │
    ▼
get_db() 호출
    │
    ▼
세션 생성 ─────────────────┐
    │                      │
    ▼                      │
yield session (세션 제공)   │ try 블록
    │                      │
    ▼                      │
라우터 함수 실행           │
    │                      │
    ▼                      │
commit() ──────────────────┘
    │
    ▼
세션 종료

예외 발생 시:
    │
    ▼
rollback() → 변경 취소
    │
    ▼
예외 전파 → 에러 응답
```

---

## 4. 모델 정의

### 4.1 기본 모델 구조

```python
# app/models/user.py

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
# Base: 모든 모델이 상속받는 베이스 클래스

# TYPE_CHECKING: 타입 힌트 순환 참조 방지용
if TYPE_CHECKING:
    from app.models.item import Item
    # 런타임에는 import 하지 않고, 타입 체크 시에만 import
    # 순환 import 문제 해결


class User(Base):
    """
    사용자 모델

    이 클래스는 데이터베이스의 'users' 테이블과 매핑됩니다.
    """

    # ========================================================
    # 테이블 이름 설정
    # ========================================================
    __tablename__ = "users"
    # __tablename__: 데이터베이스에서 사용할 테이블 이름
    # 보통 모델 이름의 복수형 소문자 사용


    # ========================================================
    # 컬럼 정의
    # ========================================================

    # 기본 키 (Primary Key)
    id: Mapped[int] = mapped_column(primary_key=True)
    # Mapped[int]: 이 컬럼의 Python 타입은 int
    # mapped_column(): SQLAlchemy 2.0 스타일 컬럼 정의
    # primary_key=True: 기본 키로 설정 (자동 증가)

    # 이메일 (유니크, 인덱스)
    email: Mapped[str] = mapped_column(
        String(255),     # VARCHAR(255) - 최대 255자
        unique=True,     # 중복 불가
        index=True,      # 인덱스 생성 (검색 성능 향상)
        nullable=False,  # NULL 불가 (필수 값)
    )

    # 사용자명
    username: Mapped[str] = mapped_column(
        String(50),      # 최대 50자
        unique=True,     # 중복 불가
        nullable=False,
    )

    # 비밀번호 해시
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # 활성 상태
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,    # Python 기본값
    )
    # default=True: INSERT 시 값을 지정하지 않으면 True 사용

    # 생성 시간
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),     # 타임존 포함 DATETIME
        server_default=func.now(),   # 데이터베이스 서버 시간
    )
    # DateTime(timezone=True): 타임존 정보 포함
    # server_default=func.now():
    #   - DB 서버에서 현재 시간 자동 설정
    #   - default=datetime.now() 대신 사용 (더 정확함)

    # 수정 시간 (선택적)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),   # UPDATE 시 자동 갱신
        nullable=True,
    )
    # Mapped[Optional[datetime]]: NULL 허용 타입
    # onupdate=func.now(): 레코드 수정 시 자동으로 현재 시간 설정


    # ========================================================
    # 관계 정의 (Relationship)
    # ========================================================

    items: Mapped[List["Item"]] = relationship(
        "Item",                      # 관계 대상 모델명 (문자열)
        back_populates="owner",      # Item 모델의 관계 속성명
        cascade="all, delete-orphan", # 삭제 시 연관 항목도 삭제
        lazy="selectin",             # 로딩 전략
    )
    # Mapped[List["Item"]]: 여러 Item과 일대다 관계
    # relationship(): 관계 정의
    # back_populates="owner": 양방향 관계 설정
    # cascade="all, delete-orphan":
    #   - User 삭제 시 관련 Item도 모두 삭제
    # lazy="selectin":
    #   - "select": 접근 시 별도 쿼리 (N+1 문제 발생 가능)
    #   - "selectin": IN 절로 한 번에 로드
    #   - "joined": JOIN으로 함께 로드
    #   - "subquery": 서브쿼리로 로드


    # ========================================================
    # 메서드 정의
    # ========================================================

    def __repr__(self) -> str:
        """디버깅용 문자열 표현"""
        return f"<User(id={self.id}, email={self.email})>"
```

### 4.2 Mapped와 mapped_column 이해하기

```python
# SQLAlchemy 2.0 스타일 (권장)
class User(Base):
    __tablename__ = "users"

    # Mapped[타입]으로 Python 타입 명시
    id: Mapped[int] = mapped_column(primary_key=True)

    # Optional로 NULL 허용
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # 기본값 지정
    is_active: Mapped[bool] = mapped_column(default=True)


# SQLAlchemy 1.x 스타일 (이전 버전, 참고용)
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    bio = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
```

**비교:**
| 특징 | 2.0 스타일 | 1.x 스타일 |
|------|-----------|-----------|
| 타입 힌트 | `Mapped[int]` | 없음 |
| 컬럼 정의 | `mapped_column()` | `Column()` |
| IDE 지원 | 자동완성 우수 | 제한적 |
| 타입 체크 | mypy 호환 | 어려움 |

### 4.3 다양한 컬럼 타입

```python
from sqlalchemy import (
    String,      # VARCHAR - 가변 길이 문자열
    Text,        # TEXT - 긴 텍스트
    Integer,     # INT - 정수
    BigInteger,  # BIGINT - 큰 정수
    Float,       # FLOAT - 부동소수점
    Numeric,     # DECIMAL - 정밀 소수점 (금액용)
    Boolean,     # BOOLEAN - 참/거짓
    DateTime,    # DATETIME - 날짜+시간
    Date,        # DATE - 날짜만
    Time,        # TIME - 시간만
    JSON,        # JSON - JSON 데이터
    LargeBinary, # BLOB - 바이너리 데이터
    Enum,        # ENUM - 열거형
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY  # PostgreSQL 전용


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 문자열
    name: Mapped[str] = mapped_column(String(200))
    # String(200): 최대 200자 VARCHAR

    description: Mapped[Optional[str]] = mapped_column(Text)
    # Text: 길이 제한 없는 텍스트 (긴 설명용)

    # 숫자
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    # Integer: 일반 정수 (-2^31 ~ 2^31-1)

    view_count: Mapped[int] = mapped_column(BigInteger, default=0)
    # BigInteger: 큰 정수 (조회수 등)

    rating: Mapped[float] = mapped_column(Float, default=0.0)
    # Float: 부동소수점 (정밀도 낮음)

    price: Mapped[float] = mapped_column(Numeric(10, 2))
    # Numeric(10, 2): 총 10자리, 소수점 2자리
    # 예: 12345678.99 (금액에 적합)

    # 불리언
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    # 날짜/시간
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    release_date: Mapped[Optional[date]] = mapped_column(Date)
    # Date: 날짜만 (2024-01-15)

    # JSON (유연한 데이터 저장)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)
    # JSON: {"color": "red", "size": "M"} 형태로 저장
    # Python dict ↔ JSON 자동 변환
```

### 4.4 관계 정의 (Relationships)

```python
# app/models/item.py

from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Item(Base):
    """
    아이템 모델 - User와 다대일 관계

    여러 Item이 하나의 User에 속함
    """
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(String(1000))

    # ========================================================
    # 외래 키 (Foreign Key)
    # ========================================================
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        # ForeignKey("테이블명.컬럼명"): 외래 키 설정
        # ondelete="CASCADE": User 삭제 시 관련 Item도 삭제
        #
        # ondelete 옵션:
        # - "CASCADE": 부모 삭제 시 자식도 삭제
        # - "SET NULL": 부모 삭제 시 NULL로 설정
        # - "RESTRICT": 자식 있으면 부모 삭제 불가

        index=True,
        # 외래 키에 인덱스 추가 (조인 성능 향상)
    )

    # ========================================================
    # 관계 정의 (다대일)
    # ========================================================
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="items",
        # back_populates: User 모델의 'items' 속성과 연결
    )
    # 사용법: item.owner.email


# ============================================================
# 관계 유형 정리
# ============================================================

# 1. 일대다 (One-to-Many): User ─< Item
#    - 한 User가 여러 Item을 가짐
#    - User 측: items: Mapped[List["Item"]] = relationship(...)
#    - Item 측: owner: Mapped["User"] = relationship(...)

# 2. 다대일 (Many-to-One): Item >─ User
#    - 위의 반대 방향

# 3. 일대일 (One-to-One): User ─ Profile
#    - uselist=False 옵션 사용
#    profile: Mapped["Profile"] = relationship(..., uselist=False)

# 4. 다대다 (Many-to-Many): User ─< >─ Role
#    - 중간 테이블 필요 (아래 예시)
```

### 4.5 다대다 관계

```python
# 다대다 관계: User ↔ Role

from sqlalchemy import Table, Column, ForeignKey

# 중간 테이블 (Association Table)
user_roles = Table(
    "user_roles",          # 테이블 이름
    Base.metadata,         # Base의 메타데이터에 등록
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)
# 복합 기본 키: (user_id, role_id) 조합이 고유


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    # 다대다 관계
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_roles,  # 중간 테이블 지정
        back_populates="roles",
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # 다대다 관계
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary=user_roles,  # 같은 중간 테이블 지정
        back_populates="users",
    )


# 사용 예시:
# user.roles.append(admin_role)  # 역할 추가
# user.roles.remove(guest_role)  # 역할 제거
# for role in user.roles:        # 사용자의 모든 역할 조회
#     print(role.name)
```

---

## 5. CRUD 작업

### 5.1 Create (생성)

```python
# app/services/user_service.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(
    db: AsyncSession,        # 데이터베이스 세션
    user_data: UserCreate,   # Pydantic 스키마
) -> User:
    """
    새 사용자 생성

    Args:
        db: 데이터베이스 세션
        user_data: 사용자 생성 데이터 (email, username, password)

    Returns:
        생성된 User 객체
    """

    # 1. User 객체 생성
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        # 비밀번호는 해시화하여 저장
    )
    # User(...): 모델 인스턴스 생성
    # 아직 DB에 저장되지 않음

    # 2. 세션에 추가
    db.add(user)
    # db.add(): 세션의 "pending" 상태에 추가
    # 트랜잭션에 포함됨

    # 3. 즉시 DB에 반영 (커밋 전)
    await db.flush()
    # flush(): INSERT 쿼리 실행
    # 아직 커밋되지 않음 (롤백 가능)
    # user.id가 생성됨

    # 4. 객체 새로고침
    await db.refresh(user)
    # refresh(): DB에서 최신 데이터 다시 로드
    # server_default 값 등을 가져옴

    return user
    # 커밋은 get_db()의 yield 이후에 자동 실행됨


# 여러 개 한 번에 생성
async def create_users_bulk(
    db: AsyncSession,
    users_data: list[UserCreate],
) -> list[User]:
    """여러 사용자 일괄 생성"""

    users = [
        User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
        )
        for data in users_data
    ]

    db.add_all(users)  # 여러 개 한 번에 추가
    await db.flush()

    for user in users:
        await db.refresh(user)

    return users
```

### 5.2 Read (조회)

```python
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload


# ============================================================
# 단일 조회
# ============================================================

async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    """ID로 사용자 조회"""

    # select() 문 생성
    stmt = select(User).where(User.id == user_id)
    # select(User): SELECT * FROM users
    # .where(User.id == user_id): WHERE id = ?

    # 쿼리 실행
    result = await db.execute(stmt)
    # db.execute(): SQL 실행
    # result: 결과 객체

    # 결과 추출
    return result.scalar_one_or_none()
    # scalar_one_or_none():
    #   - 결과 1개: User 객체 반환
    #   - 결과 0개: None 반환
    #   - 결과 2개 이상: 예외 발생


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    """이메일로 사용자 조회"""

    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


# ============================================================
# 목록 조회
# ============================================================

async def get_users(
    db: AsyncSession,
    skip: int = 0,     # 건너뛸 개수 (offset)
    limit: int = 100,  # 가져올 개수
) -> list[User]:
    """사용자 목록 조회 (페이징)"""

    result = await db.execute(
        select(User)
        .offset(skip)   # OFFSET skip
        .limit(limit)   # LIMIT limit
        .order_by(User.created_at.desc())  # 최신순 정렬
    )
    # .offset(skip): 처음 skip개 건너뛰기
    # .limit(limit): 최대 limit개만 가져오기
    # .order_by(...): 정렬
    # .desc(): 내림차순 (최신순)
    # .asc(): 오름차순 (오래된순)

    return list(result.scalars().all())
    # result.scalars(): 단일 컬럼(User 객체) 추출
    # .all(): 모든 결과를 리스트로
    # list(): 명시적 리스트 변환


# ============================================================
# 조건 조회
# ============================================================

async def get_active_users(
    db: AsyncSession,
) -> list[User]:
    """활성 사용자만 조회"""

    result = await db.execute(
        select(User).where(User.is_active == True)
        # == True: 정확한 비교 (== 연산자 오버로딩)
    )
    return list(result.scalars().all())


async def search_users(
    db: AsyncSession,
    keyword: str,
) -> list[User]:
    """사용자 검색 (이메일 또는 이름)"""

    result = await db.execute(
        select(User).where(
            # OR 조건
            (User.email.ilike(f"%{keyword}%")) |
            (User.username.ilike(f"%{keyword}%"))
        )
    )
    # .ilike(): 대소문자 무시 LIKE
    # f"%{keyword}%": 부분 일치 검색
    # |: OR 연산자
    # &: AND 연산자

    return list(result.scalars().all())


# ============================================================
# 관계 데이터 함께 로드 (Eager Loading)
# ============================================================

async def get_user_with_items(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    """사용자와 아이템 함께 조회"""

    result = await db.execute(
        select(User)
        .options(selectinload(User.items))  # items 관계 미리 로드
        .where(User.id == user_id)
    )
    # selectinload(): SELECT ... WHERE id IN (...) 쿼리로 로드
    # 장점: N+1 문제 방지

    return result.unique().scalar_one_or_none()
    # .unique(): 중복 제거 (관계 로드 시 필요)


# Eager Loading 옵션 비교:
#
# selectinload(User.items)
#   - 2개의 쿼리 실행
#   - SELECT * FROM users WHERE id = ?
#   - SELECT * FROM items WHERE owner_id IN (?)
#   - 대부분의 경우 권장
#
# joinedload(User.items)
#   - 1개의 JOIN 쿼리
#   - SELECT ... FROM users LEFT JOIN items ON ...
#   - 일대일 관계에 적합
#
# lazyload (기본값)
#   - 접근 시점에 쿼리
#   - user.items 접근 시 SELECT 실행
#   - N+1 문제 발생 가능


# ============================================================
# 집계 함수
# ============================================================

async def count_users(db: AsyncSession) -> int:
    """전체 사용자 수"""

    result = await db.execute(
        select(func.count(User.id))
        # func.count(): COUNT 함수
    )
    return result.scalar() or 0
    # .scalar(): 단일 값 반환


async def count_active_users(db: AsyncSession) -> int:
    """활성 사용자 수"""

    result = await db.execute(
        select(func.count(User.id))
        .where(User.is_active == True)
    )
    return result.scalar() or 0
```

### 5.3 Update (수정)

```python
from app.schemas.user import UserUpdate


async def update_user(
    db: AsyncSession,
    user: User,               # 수정할 User 객체
    user_data: UserUpdate,    # 수정 데이터
) -> User:
    """사용자 정보 수정"""

    # 방법 1: 속성 직접 수정
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    # 변경 사항 DB에 반영
    await db.flush()
    await db.refresh(user)

    return user
    # SQLAlchemy가 변경 사항 자동 추적
    # flush() 시 UPDATE 쿼리 실행


async def update_user_v2(
    db: AsyncSession,
    user_id: int,
    update_data: dict,
) -> User | None:
    """딕셔너리로 사용자 수정"""

    # 먼저 조회
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    # 딕셔너리로 업데이트
    for key, value in update_data.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    # setattr(user, 'email', 'new@example.com')
    # == user.email = 'new@example.com'

    await db.flush()
    await db.refresh(user)

    return user


# ============================================================
# 벌크 업데이트 (여러 레코드 한 번에)
# ============================================================

from sqlalchemy import update

async def deactivate_old_users(
    db: AsyncSession,
    days: int = 365,
) -> int:
    """오래된 사용자 비활성화"""

    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days)

    result = await db.execute(
        update(User)
        .where(User.created_at < cutoff_date)
        .where(User.is_active == True)
        .values(is_active=False)
    )
    # update(User): UPDATE users
    # .where(...): WHERE 조건
    # .values(is_active=False): SET is_active = false

    await db.flush()

    return result.rowcount
    # rowcount: 영향받은 행 수
```

### 5.4 Delete (삭제)

```python
from sqlalchemy import delete


async def delete_user(
    db: AsyncSession,
    user: User,
) -> None:
    """사용자 삭제 (객체로)"""

    await db.delete(user)
    # db.delete(): DELETE 마킹
    # cascade 설정에 따라 관련 데이터도 삭제

    await db.flush()


async def delete_user_by_id(
    db: AsyncSession,
    user_id: int,
) -> bool:
    """사용자 삭제 (ID로)"""

    # 방법 1: 객체 조회 후 삭제
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.flush()
    return True


async def delete_user_direct(
    db: AsyncSession,
    user_id: int,
) -> bool:
    """사용자 직접 삭제 (조회 없이)"""

    result = await db.execute(
        delete(User).where(User.id == user_id)
    )
    # delete(User): DELETE FROM users
    # .where(...): WHERE 조건

    await db.flush()

    return result.rowcount > 0
    # rowcount: 삭제된 행 수


# ============================================================
# 소프트 삭제 (Soft Delete)
# ============================================================

async def soft_delete_user(
    db: AsyncSession,
    user_id: int,
) -> bool:
    """
    소프트 삭제: 실제로 삭제하지 않고 deleted_at 설정

    이점:
    - 데이터 복구 가능
    - 감사 추적 가능
    - 관련 데이터 참조 무결성 유지
    """

    from datetime import datetime

    result = await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(deleted_at=datetime.now())
    )

    await db.flush()
    return result.rowcount > 0


# 소프트 삭제된 레코드 제외하고 조회
async def get_active_users_soft(db: AsyncSession) -> list[User]:
    """삭제되지 않은 사용자만 조회"""

    result = await db.execute(
        select(User).where(User.deleted_at.is_(None))
        # .is_(None): IS NULL
        # == None 대신 .is_(None) 사용
    )
    return list(result.scalars().all())
```

---

## 6. 고급 쿼리

### 6.1 복잡한 WHERE 조건

```python
from sqlalchemy import select, and_, or_, not_


async def complex_query_example(db: AsyncSession):
    """복잡한 조건 쿼리 예시"""

    # AND 조건
    result = await db.execute(
        select(User).where(
            and_(
                User.is_active == True,
                User.email.like("%@example.com"),
            )
        )
    )
    # WHERE is_active = true AND email LIKE '%@example.com'

    # OR 조건
    result = await db.execute(
        select(User).where(
            or_(
                User.email.like("%@admin.com"),
                User.username == "admin",
            )
        )
    )
    # WHERE email LIKE '%@admin.com' OR username = 'admin'

    # NOT 조건
    result = await db.execute(
        select(User).where(
            not_(User.is_active)
        )
    )
    # WHERE NOT is_active

    # IN 조건
    user_ids = [1, 2, 3, 4, 5]
    result = await db.execute(
        select(User).where(User.id.in_(user_ids))
    )
    # WHERE id IN (1, 2, 3, 4, 5)

    # NOT IN 조건
    result = await db.execute(
        select(User).where(User.id.not_in(user_ids))
    )
    # WHERE id NOT IN (1, 2, 3, 4, 5)

    # BETWEEN 조건
    from datetime import datetime, timedelta

    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()

    result = await db.execute(
        select(User).where(
            User.created_at.between(start_date, end_date)
        )
    )
    # WHERE created_at BETWEEN ? AND ?

    # NULL 체크
    result = await db.execute(
        select(User).where(User.deleted_at.is_(None))
    )
    # WHERE deleted_at IS NULL

    result = await db.execute(
        select(User).where(User.deleted_at.is_not(None))
    )
    # WHERE deleted_at IS NOT NULL

    # LIKE 패턴
    result = await db.execute(
        select(User).where(User.email.like("admin%"))  # 시작
    )
    # WHERE email LIKE 'admin%'

    result = await db.execute(
        select(User).where(User.email.ilike("%ADMIN%"))  # 대소문자 무시
    )
    # WHERE email ILIKE '%ADMIN%' (PostgreSQL)
    # WHERE LOWER(email) LIKE LOWER('%ADMIN%') (SQLite)
```

### 6.2 정렬과 페이징

```python
from sqlalchemy import desc, asc, nullsfirst, nullslast


async def sorted_query_example(db: AsyncSession):
    """정렬 쿼리 예시"""

    # 단일 정렬
    result = await db.execute(
        select(User).order_by(User.created_at.desc())
    )
    # ORDER BY created_at DESC

    # 여러 컬럼 정렬
    result = await db.execute(
        select(User).order_by(
            User.is_active.desc(),  # 활성 사용자 먼저
            User.created_at.desc(), # 최신순
        )
    )
    # ORDER BY is_active DESC, created_at DESC

    # NULL 처리
    result = await db.execute(
        select(User).order_by(
            User.updated_at.desc().nullslast()
        )
    )
    # ORDER BY updated_at DESC NULLS LAST
    # NULL 값을 맨 뒤로

    # 페이징
    page = 1
    per_page = 20

    result = await db.execute(
        select(User)
        .order_by(User.id)
        .offset((page - 1) * per_page)  # 건너뛸 개수
        .limit(per_page)                 # 가져올 개수
    )
    # LIMIT 20 OFFSET 0 (1페이지)
    # LIMIT 20 OFFSET 20 (2페이지)


async def get_paginated_users(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[User], int]:
    """페이징된 사용자 목록과 전체 수"""

    # 전체 수 조회
    total_result = await db.execute(
        select(func.count(User.id))
    )
    total = total_result.scalar() or 0

    # 페이징된 목록 조회
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    users = list(result.scalars().all())

    return users, total
```

### 6.3 집계와 그룹화

```python
from sqlalchemy import func, case


async def aggregation_examples(db: AsyncSession):
    """집계 쿼리 예시"""

    # COUNT
    result = await db.execute(
        select(func.count(User.id))
    )
    total_users = result.scalar()
    # SELECT COUNT(id) FROM users

    # COUNT with DISTINCT
    result = await db.execute(
        select(func.count(func.distinct(User.email)))
    )
    unique_emails = result.scalar()
    # SELECT COUNT(DISTINCT email) FROM users

    # SUM, AVG, MIN, MAX
    result = await db.execute(
        select(
            func.sum(Item.price),
            func.avg(Item.price),
            func.min(Item.price),
            func.max(Item.price),
        )
    )
    total, average, minimum, maximum = result.one()

    # GROUP BY
    result = await db.execute(
        select(
            User.is_active,
            func.count(User.id).label("count")
        )
        .group_by(User.is_active)
    )
    # SELECT is_active, COUNT(id) AS count
    # FROM users
    # GROUP BY is_active

    for row in result:
        print(f"is_active={row.is_active}, count={row.count}")

    # HAVING
    result = await db.execute(
        select(
            Item.owner_id,
            func.count(Item.id).label("item_count")
        )
        .group_by(Item.owner_id)
        .having(func.count(Item.id) > 5)
    )
    # HAVING: GROUP BY 결과에 조건
    # COUNT(id) > 5인 owner_id만 반환

    # CASE WHEN
    result = await db.execute(
        select(
            User.id,
            case(
                (User.is_active == True, "활성"),
                (User.is_active == False, "비활성"),
                else_="알 수 없음"
            ).label("status")
        )
    )
    # SELECT id, CASE WHEN is_active = true THEN '활성' ... END AS status
```

### 6.4 조인 (JOIN)

```python
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def join_examples(db: AsyncSession):
    """JOIN 쿼리 예시"""

    # ========================================================
    # ORM 스타일: relationship + options
    # ========================================================

    # User의 items 함께 로드
    result = await db.execute(
        select(User)
        .options(joinedload(User.items))  # LEFT JOIN
        .where(User.id == 1)
    )
    user = result.unique().scalar_one_or_none()
    # user.items에 접근 가능 (추가 쿼리 없이)


    # ========================================================
    # 명시적 JOIN
    # ========================================================

    # INNER JOIN
    result = await db.execute(
        select(User, Item)
        .join(Item, User.id == Item.owner_id)
        # join(): INNER JOIN (매칭되는 것만)
    )
    for user, item in result:
        print(f"{user.email}: {item.title}")

    # LEFT JOIN
    result = await db.execute(
        select(User, Item)
        .outerjoin(Item, User.id == Item.owner_id)
        # outerjoin(): LEFT OUTER JOIN
    )
    for user, item in result:
        if item:
            print(f"{user.email}: {item.title}")
        else:
            print(f"{user.email}: 아이템 없음")


    # ========================================================
    # 특정 컬럼만 선택
    # ========================================================

    result = await db.execute(
        select(User.email, Item.title)
        .join(Item, User.id == Item.owner_id)
    )
    for email, title in result:
        print(f"{email}: {title}")


    # ========================================================
    # 서브쿼리
    # ========================================================

    # 아이템이 있는 사용자만 조회
    subquery = (
        select(Item.owner_id)
        .distinct()
        .scalar_subquery()
    )

    result = await db.execute(
        select(User)
        .where(User.id.in_(subquery))
    )
    # WHERE id IN (SELECT DISTINCT owner_id FROM items)


    # ========================================================
    # CTE (Common Table Expression)
    # ========================================================

    from sqlalchemy import cte

    # 아이템 수 집계
    item_counts = (
        select(
            Item.owner_id,
            func.count(Item.id).label("item_count")
        )
        .group_by(Item.owner_id)
        .cte("item_counts")
    )

    # CTE 사용
    result = await db.execute(
        select(User, item_counts.c.item_count)
        .outerjoin(item_counts, User.id == item_counts.c.owner_id)
    )
    # WITH item_counts AS (...)
    # SELECT ... FROM users LEFT JOIN item_counts ON ...
```

---

## 7. 마이그레이션 (Alembic)

### 7.1 Alembic 소개

Alembic은 SQLAlchemy의 **데이터베이스 마이그레이션 도구**입니다.

```
마이그레이션이란?
- 데이터베이스 스키마(구조) 변경을 관리
- 버전 관리처럼 변경 이력 추적
- 롤백(되돌리기) 가능
```

### 7.2 초기 설정

```bash
# Alembic 초기화
alembic init alembic
# alembic/ 폴더와 alembic.ini 파일 생성
```

프로젝트 구조:
```
project/
├── alembic/
│   ├── versions/        # 마이그레이션 파일들
│   ├── env.py           # 환경 설정
│   └── script.py.mako   # 템플릿
├── alembic.ini          # Alembic 설정
└── app/
    └── ...
```

### 7.3 alembic.ini 설정

```ini
# alembic.ini

[alembic]
# 마이그레이션 스크립트 위치
script_location = alembic

# 데이터베이스 URL
sqlalchemy.url = sqlite+aiosqlite:///./app.db

# 로깅 설정
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

### 7.4 env.py 설정 (비동기)

```python
# alembic/env.py

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 프로젝트의 Base와 모델 import
from app.database import Base
from app.models import user, item  # 모든 모델 import 필요!

# Alembic 설정
config = context.config

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 메타데이터 설정 (자동 생성에 필요)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """오프라인 모드 (SQL 생성만)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """실제 마이그레이션 실행"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """비동기 마이그레이션 실행"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """온라인 모드 (실제 DB 적용)"""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 7.5 마이그레이션 명령어

```bash
# ============================================================
# 마이그레이션 생성
# ============================================================

# 자동 생성 (모델 변경 감지)
alembic revision --autogenerate -m "Add users table"
# --autogenerate: 모델과 DB 비교하여 자동 생성
# -m "설명": 마이그레이션 설명

# 수동 생성 (빈 파일)
alembic revision -m "Custom migration"


# ============================================================
# 마이그레이션 적용
# ============================================================

# 최신 버전으로 업그레이드
alembic upgrade head
# head: 가장 최신 버전

# 특정 버전으로 업그레이드
alembic upgrade abc123
# abc123: 버전 ID

# 한 단계씩 업그레이드
alembic upgrade +1


# ============================================================
# 마이그레이션 롤백
# ============================================================

# 한 단계 롤백
alembic downgrade -1

# 특정 버전으로 롤백
alembic downgrade abc123

# 처음으로 롤백
alembic downgrade base


# ============================================================
# 상태 확인
# ============================================================

# 현재 버전 확인
alembic current

# 히스토리 확인
alembic history

# 적용 예정 변경사항 확인
alembic upgrade head --sql
# --sql: 실행할 SQL만 출력 (실제 적용 안 함)
```

### 7.6 마이그레이션 파일 예시

```python
# alembic/versions/xxxx_add_users_table.py

"""Add users table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2024-01-15 10:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = None  # 이전 버전 (없으면 None)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    업그레이드: 테이블 생성

    alembic upgrade 시 실행
    """
    op.create_table(
        'users',  # 테이블 이름
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        ),
    )
    # op.create_table(): CREATE TABLE
    # sa.Column(): 컬럼 정의

    # 인덱스 생성
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # op.create_index(): CREATE INDEX
    # unique=True: UNIQUE INDEX

    # 유니크 제약조건
    op.create_unique_constraint('uq_users_username', 'users', ['username'])


def downgrade() -> None:
    """
    다운그레이드: 테이블 삭제

    alembic downgrade 시 실행
    """
    # 인덱스 삭제
    op.drop_index('ix_users_email', 'users')

    # 유니크 제약조건 삭제
    op.drop_constraint('uq_users_username', 'users')

    # 테이블 삭제
    op.drop_table('users')
```

### 7.7 일반적인 마이그레이션 작업

```python
# ============================================================
# 컬럼 추가
# ============================================================

def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('bio', sa.String(500), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('users', 'bio')


# ============================================================
# 컬럼 수정
# ============================================================

def upgrade() -> None:
    # 컬럼 타입 변경
    op.alter_column(
        'users',
        'username',
        type_=sa.String(100),  # 50 → 100
        existing_type=sa.String(50),
    )

    # nullable 변경
    op.alter_column(
        'users',
        'bio',
        nullable=False,
        existing_nullable=True,
    )

def downgrade() -> None:
    op.alter_column(
        'users',
        'username',
        type_=sa.String(50),
        existing_type=sa.String(100),
    )
    op.alter_column(
        'users',
        'bio',
        nullable=True,
        existing_nullable=False,
    )


# ============================================================
# 컬럼 삭제
# ============================================================

def upgrade() -> None:
    op.drop_column('users', 'deprecated_field')

def downgrade() -> None:
    op.add_column(
        'users',
        sa.Column('deprecated_field', sa.String(100))
    )


# ============================================================
# 테이블 이름 변경
# ============================================================

def upgrade() -> None:
    op.rename_table('old_name', 'new_name')

def downgrade() -> None:
    op.rename_table('new_name', 'old_name')


# ============================================================
# 외래 키 추가
# ============================================================

def upgrade() -> None:
    op.add_column(
        'items',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'fk_items_owner_id',     # 제약조건 이름
        'items',                  # 소스 테이블
        'users',                  # 참조 테이블
        ['owner_id'],             # 소스 컬럼
        ['id'],                   # 참조 컬럼
        ondelete='CASCADE',       # 삭제 시 동작
    )

def downgrade() -> None:
    op.drop_constraint('fk_items_owner_id', 'items', type_='foreignkey')
    op.drop_column('items', 'owner_id')


# ============================================================
# 데이터 마이그레이션 (기존 데이터 변환)
# ============================================================

def upgrade() -> None:
    # 새 컬럼 추가
    op.add_column('users', sa.Column('full_name', sa.String(100)))

    # 기존 데이터 업데이트
    op.execute(
        "UPDATE users SET full_name = username WHERE full_name IS NULL"
    )

    # NOT NULL로 변경
    op.alter_column('users', 'full_name', nullable=False)

def downgrade() -> None:
    op.drop_column('users', 'full_name')
```

---

## 8. 트랜잭션

### 8.1 트랜잭션 기본 개념

```
트랜잭션이란?
- 여러 DB 작업을 하나의 단위로 묶음
- 모두 성공하거나, 모두 실패 (원자성)
- ACID 특성 보장
```

```
ACID:
- Atomicity (원자성): 전부 성공 또는 전부 실패
- Consistency (일관성): 트랜잭션 전후 데이터 일관성 유지
- Isolation (격리성): 동시 트랜잭션 간 간섭 방지
- Durability (지속성): 커밋된 데이터는 영구 저장
```

### 8.2 자동 트랜잭션 (의존성)

```python
# get_db() 의존성이 자동으로 트랜잭션 관리

@router.post("/users")
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    이 라우터 함수는 하나의 트랜잭션으로 실행됨
    - 성공 시: 자동 commit
    - 실패 시: 자동 rollback
    """
    user = await user_service.create_user(db, user_data)
    items = await item_service.create_items(db, user.id, default_items)

    return user
    # 모든 작업이 성공하면 commit
    # 중간에 에러 발생 시 전체 rollback
```

### 8.3 명시적 트랜잭션

```python
async def transfer_items(
    db: AsyncSession,
    from_user_id: int,
    to_user_id: int,
    item_ids: list[int],
) -> bool:
    """
    아이템 소유권 이전 (트랜잭션 필수)

    모든 아이템이 성공적으로 이전되거나,
    하나라도 실패하면 전체 취소
    """

    try:
        # 명시적 트랜잭션 시작
        async with db.begin():
            # begin(): 새 트랜잭션 시작
            # with 블록 끝에서 자동 commit
            # 예외 발생 시 자동 rollback

            # from_user 확인
            from_user = await get_user_by_id(db, from_user_id)
            if not from_user:
                raise ValueError("보내는 사용자가 없습니다")

            # to_user 확인
            to_user = await get_user_by_id(db, to_user_id)
            if not to_user:
                raise ValueError("받는 사용자가 없습니다")

            # 아이템들 이전
            for item_id in item_ids:
                item = await get_item_by_id(db, item_id)

                if not item:
                    raise ValueError(f"아이템 {item_id}를 찾을 수 없습니다")

                if item.owner_id != from_user_id:
                    raise ValueError(f"아이템 {item_id}의 소유자가 아닙니다")

                item.owner_id = to_user_id

            # 모든 변경 적용
            await db.flush()

        # with 블록 끝 → 자동 commit
        return True

    except Exception as e:
        # 예외 발생 → 자동 rollback
        print(f"이전 실패: {e}")
        return False
```

### 8.4 중첩 트랜잭션 (Savepoint)

```python
async def complex_operation(db: AsyncSession):
    """
    중첩 트랜잭션 예시

    부분적 롤백이 필요한 경우 사용
    """

    async with db.begin():
        # 외부 트랜잭션 시작

        # 반드시 수행해야 할 작업
        user = await create_user(db, main_user_data)

        try:
            # Savepoint 생성
            async with db.begin_nested():
                # begin_nested(): SAVEPOINT 생성

                # 실패해도 되는 선택적 작업
                await create_optional_data(db, user.id)

        except Exception:
            # Savepoint로 롤백
            # 외부 트랜잭션은 유지됨
            pass

        # user 생성은 유지됨
        # optional_data는 롤백됨 (실패 시)
```

---

## 9. 성능 최적화

### 9.1 N+1 문제와 해결

```python
# ============================================================
# N+1 문제 예시
# ============================================================

async def bad_example(db: AsyncSession):
    """N+1 문제가 발생하는 코드"""

    result = await db.execute(select(User))
    users = result.scalars().all()
    # 1번의 쿼리: SELECT * FROM users

    for user in users:
        print(f"User: {user.email}")

        # 각 user마다 추가 쿼리 발생!
        for item in user.items:
            print(f"  - {item.title}")

    # 총 쿼리 수: 1 + N (사용자 수만큼 추가 쿼리)


# ============================================================
# 해결: Eager Loading
# ============================================================

async def good_example(db: AsyncSession):
    """Eager Loading으로 N+1 해결"""

    result = await db.execute(
        select(User)
        .options(selectinload(User.items))
    )
    users = result.scalars().unique().all()
    # 2번의 쿼리:
    # 1. SELECT * FROM users
    # 2. SELECT * FROM items WHERE owner_id IN (1, 2, 3, ...)

    for user in users:
        print(f"User: {user.email}")

        # 추가 쿼리 없음!
        for item in user.items:
            print(f"  - {item.title}")


# ============================================================
# Eager Loading 선택 가이드
# ============================================================

# selectinload: 별도 SELECT ... WHERE IN 쿼리
# - 대부분의 경우 권장
# - 다대다, 일대다 관계에 적합
result = await db.execute(
    select(User).options(selectinload(User.items))
)

# joinedload: LEFT OUTER JOIN
# - 일대일, 다대일 관계에 적합
# - 데이터 중복 가능성 있음
result = await db.execute(
    select(Item).options(joinedload(Item.owner))
)

# subqueryload: 서브쿼리
# - 큰 데이터셋에서 selectinload보다 효율적일 수 있음
result = await db.execute(
    select(User).options(subqueryload(User.items))
)
```

### 9.2 인덱스 활용

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 단일 컬럼 인덱스
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,  # 인덱스 생성
    )

    # 복합 인덱스 (테이블 레벨)
    __table_args__ = (
        Index('ix_user_search', 'username', 'email'),
        # 2개 이상의 컬럼으로 인덱스
        # WHERE username = ? AND email = ? 쿼리에 효과적
    )


# 인덱스가 효과적인 경우:
# - WHERE 조건에 자주 사용되는 컬럼
# - JOIN 조건에 사용되는 컬럼
# - ORDER BY에 사용되는 컬럼
# - UNIQUE 제약조건이 필요한 컬럼

# 인덱스가 비효과적인 경우:
# - 데이터가 적은 테이블
# - 자주 INSERT/UPDATE되는 테이블
# - 카디널리티(고유값 수)가 낮은 컬럼 (예: is_active)
```

### 9.3 쿼리 최적화

```python
# ============================================================
# 필요한 컬럼만 선택
# ============================================================

# 나쁜 예: 모든 컬럼 조회
result = await db.execute(select(User))
# SELECT * FROM users

# 좋은 예: 필요한 컬럼만
result = await db.execute(
    select(User.id, User.email)
)
# SELECT id, email FROM users


# ============================================================
# EXISTS 사용
# ============================================================

# 나쁜 예: 전체 카운트
result = await db.execute(
    select(func.count(User.id))
    .where(User.email == email)
)
exists = (result.scalar() or 0) > 0

# 좋은 예: EXISTS (첫 번째 결과만 확인)
from sqlalchemy import exists

result = await db.execute(
    select(
        exists()
        .where(User.email == email)
    )
)
email_exists = result.scalar()


# ============================================================
# 벌크 연산
# ============================================================

# 나쁜 예: 하나씩 업데이트
for user in users:
    user.is_active = False
    await db.flush()

# 좋은 예: 벌크 업데이트
from sqlalchemy import update

await db.execute(
    update(User)
    .where(User.id.in_(user_ids))
    .values(is_active=False)
)


# ============================================================
# 벌크 삽입
# ============================================================

# 나쁜 예: 하나씩 삽입
for data in items_data:
    item = Item(**data)
    db.add(item)
    await db.flush()

# 좋은 예: 벌크 삽입
from sqlalchemy import insert

await db.execute(
    insert(Item),
    items_data  # [{"title": "...", "owner_id": 1}, ...]
)
```

---

## 10. 테스트

### 10.1 테스트 설정

```python
# tests/conftest.py

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database import Base, get_db
from app.main import app


# 테스트용 데이터베이스 URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    """이벤트 루프 픽스처"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    테스트용 데이터베이스 세션

    각 테스트마다:
    1. 새 데이터베이스 생성
    2. 테스트 실행
    3. 데이터베이스 삭제
    """

    # 테스트용 엔진 생성
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,  # 테스트 시 SQL 로깅 끄기
    )

    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 세션 팩토리
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # 세션 제공
    async with async_session() as session:
        yield session

    # 테이블 삭제 (클린업)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    """
    테스트 클라이언트

    FastAPI의 get_db 의존성을 테스트 세션으로 교체
    """
    from httpx import AsyncClient, ASGITransport

    # 의존성 오버라이드
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    # 오버라이드 해제
    app.dependency_overrides.clear()
```

### 10.2 테스트 작성

```python
# tests/test_user_service.py

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services import user_service
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """사용자 생성 테스트"""

    # Given: 사용자 데이터
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
    )

    # When: 사용자 생성
    user = await user_service.create_user(db_session, user_data)

    # Then: 검증
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password != "password123"  # 해시됨
    assert user.is_active is True


@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    """이메일로 사용자 조회 테스트"""

    # Given: 사용자 생성
    user = User(
        email="find@example.com",
        username="findme",
        hashed_password="hashed",
    )
    db_session.add(user)
    await db_session.commit()

    # When: 이메일로 조회
    found_user = await user_service.get_user_by_email(
        db_session,
        "find@example.com"
    )

    # Then: 검증
    assert found_user is not None
    assert found_user.email == "find@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(db_session: AsyncSession):
    """존재하지 않는 사용자 조회 테스트"""

    # When: 존재하지 않는 이메일로 조회
    user = await user_service.get_user_by_email(
        db_session,
        "nonexistent@example.com"
    )

    # Then: None 반환
    assert user is None


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession):
    """사용자 수정 테스트"""

    # Given: 사용자 생성
    user = User(
        email="update@example.com",
        username="updateme",
        hashed_password="hashed",
    )
    db_session.add(user)
    await db_session.commit()

    # When: 사용자 수정
    user.email = "updated@example.com"
    await db_session.commit()

    # Then: 변경 확인
    await db_session.refresh(user)
    assert user.email == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(db_session: AsyncSession):
    """사용자 삭제 테스트"""

    # Given: 사용자 생성
    user = User(
        email="delete@example.com",
        username="deleteme",
        hashed_password="hashed",
    )
    db_session.add(user)
    await db_session.commit()
    user_id = user.id

    # When: 사용자 삭제
    await db_session.delete(user)
    await db_session.commit()

    # Then: 삭제 확인
    found_user = await user_service.get_user_by_id(db_session, user_id)
    assert found_user is None
```

---

## 11. 학습 순서 추천

1. **기초** (1주차)
   - 모델 정의 (테이블, 컬럼)
   - 기본 CRUD 작업
   - 단순 쿼리 (where, order_by)

2. **관계와 조인** (2주차)
   - 관계 정의 (일대다, 다대다)
   - Eager Loading
   - JOIN 쿼리

3. **고급 쿼리** (3주차)
   - 집계 함수
   - 복잡한 조건
   - 서브쿼리

4. **마이그레이션과 최적화** (4주차)
   - Alembic 사용
   - 인덱스 설계
   - 성능 최적화

---

## 12. 참고 자료

### 공식 문서
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy 비동기 가이드](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic 문서](https://alembic.sqlalchemy.org/en/latest/)

### 추가 학습
- [SQLAlchemy ORM 튜토리얼](https://docs.sqlalchemy.org/en/20/tutorial/)
- [FastAPI + SQLAlchemy 가이드](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

## 요약: 핵심 개념 정리

| 개념 | 설명 | 예시 |
|------|------|------|
| Base | 모든 모델의 부모 클래스 | `class User(Base):` |
| Mapped | 타입 힌트 | `id: Mapped[int]` |
| mapped_column | 컬럼 정의 | `mapped_column(primary_key=True)` |
| relationship | 관계 정의 | `relationship("Item", back_populates="owner")` |
| select | 조회 쿼리 | `select(User).where(User.id == 1)` |
| execute | 쿼리 실행 | `await db.execute(stmt)` |
| scalar_one_or_none | 단일 결과 | `result.scalar_one_or_none()` |
| scalars().all() | 목록 결과 | `list(result.scalars().all())` |
| add | 추가 | `db.add(user)` |
| flush | 변경 반영 | `await db.flush()` |
| commit | 커밋 | `await db.commit()` |
| rollback | 롤백 | `await db.rollback()` |
| delete | 삭제 | `await db.delete(user)` |
