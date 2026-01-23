"""
API Dependencies (의존성 주입)
FastAPI 의존성 주입 함수 정의

=============================================================================
의존성 주입(Dependency Injection, DI)이란?
=============================================================================
의존성 주입은 함수나 클래스가 필요로 하는 객체(의존성)를
외부에서 제공받는 디자인 패턴입니다.

예를 들어, 사용자 정보를 조회하는 API가 있다면:
- 데이터베이스 세션이 필요합니다 → get_db 의존성
- 현재 로그인한 사용자가 필요합니다 → get_current_user 의존성

FastAPI에서는 Depends()를 사용하여 의존성을 주입받습니다.

장점:
    1. 코드 재사용: 같은 의존성을 여러 곳에서 사용
    2. 테스트 용이: 테스트 시 가짜(mock) 의존성 주입 가능
    3. 관심사 분리: 인증, DB 연결 등의 로직을 분리
    4. 자동 문서화: OpenAPI 문서에 의존성 정보 포함

사용 예시:
    @app.get("/users/me")
    async def get_me(user: CurrentUser):
        # user는 get_current_user 함수의 반환값이 자동으로 주입됨
        return user
=============================================================================
"""

from typing import Annotated, Optional

from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.database import get_db
from app.models.user import User
from app.services.auth import AuthService
from app.services.item import ItemService
from app.services.user import UserService


# =============================================================================
# 데이터베이스 세션 의존성
# =============================================================================
# Annotated[타입, Depends(...)]는 Python 3.9+에서 권장되는 의존성 선언 방식입니다.
#
# 사용법:
#     async def my_endpoint(db: DbSession):
#         # db는 자동으로 AsyncSession 인스턴스가 주입됨
#         result = await db.execute(query)
#
# 동작 원리:
#     1. 요청이 들어오면 FastAPI가 get_db()를 호출
#     2. get_db()는 AsyncSession을 생성하여 반환
#     3. 요청 처리 완료 후 세션 자동 정리
# =============================================================================
DbSession = Annotated[AsyncSession, Depends(get_db)]


# =============================================================================
# 토큰 추출 함수
# =============================================================================
# httpOnly 쿠키에서 JWT 토큰을 추출합니다.
#
# 왜 쿠키를 사용하나요?
#     - httpOnly 쿠키는 JavaScript에서 접근 불가 → XSS 공격 방지
#     - 브라우저가 자동으로 쿠키를 전송 → 클라이언트 코드 간소화
#     - localStorage보다 보안성이 높음
#
# Cookie() 파라미터:
#     - 쿠키 이름이 함수 파라미터 이름과 동일해야 함 (access_token)
#     - Optional[str]로 선언하여 쿠키가 없어도 에러 발생하지 않음
# =============================================================================


async def get_token_from_cookie(
    access_token: Annotated[Optional[str], Cookie()] = None,
) -> Optional[str]:
    """
    쿠키에서 JWT 액세스 토큰 추출

    브라우저가 요청 시 자동으로 전송하는 'access_token' 쿠키에서
    JWT 토큰을 추출합니다.

    Args:
        access_token: 쿠키에서 자동으로 추출된 토큰 값
                     쿠키가 없으면 None

    Returns:
        JWT 토큰 문자열 또는 None

    Note:
        쿠키 이름 'access_token'은 로그인 시 설정한 이름과 일치해야 합니다.
        (app/api/v1/auth.py의 login 함수 참조)
    """
    return access_token


# =============================================================================
# 현재 사용자 조회 의존성
# =============================================================================
# 인증이 필요한 엔드포인트에서 사용합니다.
# 토큰이 없거나 유효하지 않으면 401 에러를 발생시킵니다.
#
# 인증 흐름:
#     1. 쿠키에서 토큰 추출 (get_token_from_cookie)
#     2. 토큰 유효성 검증 (verify_token)
#     3. 토큰에서 사용자 ID 추출
#     4. DB에서 사용자 조회
#     5. 사용자 활성 상태 확인
#     6. 사용자 객체 반환
# =============================================================================


async def get_current_user(
    db: DbSession,
    token: Annotated[Optional[str], Depends(get_token_from_cookie)],
) -> User:
    """
    현재 인증된 사용자 조회

    쿠키에서 JWT 토큰을 추출하여 사용자를 인증합니다.
    인증 실패 시 401 Unauthorized 에러를 발생시킵니다.

    Args:
        db: 데이터베이스 세션 (자동 주입)
        token: JWT 액세스 토큰 (쿠키에서 자동 추출)

    Returns:
        인증된 User 객체

    Raises:
        HTTPException 401: 다음 경우에 발생
            - 토큰이 없음 (로그인하지 않음)
            - 토큰이 만료됨
            - 토큰이 변조됨
            - 사용자가 존재하지 않음
            - 사용자가 비활성화됨

    사용 예시:
        @app.get("/protected")
        async def protected_endpoint(user: CurrentUser):
            return {"message": f"안녕하세요, {user.username}님!"}
    """
    # Step 1: 토큰 존재 확인
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},  # OAuth2 표준 헤더
        )

    # Step 2: 토큰 유효성 검증 및 페이로드 추출
    # verify_token은 토큰을 디코딩하고 서명을 검증합니다.
    # 유효하지 않으면 None을 반환합니다.
    payload = verify_token(token, token_type="access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: 페이로드에서 사용자 ID 추출
    # JWT의 'sub' (subject) 클레임에 사용자 ID가 저장되어 있습니다.
    user_id = int(payload["sub"])

    # Step 4: 데이터베이스에서 사용자 조회
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 5: 사용자 활성 상태 확인
    # 관리자가 계정을 비활성화했을 수 있습니다.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비활성화된 계정입니다.",
        )

    return user


# =============================================================================
# 선택적 사용자 조회 의존성
# =============================================================================
# 로그인 여부에 관계없이 접근 가능한 엔드포인트에서 사용합니다.
# 로그인한 사용자면 User 객체를, 아니면 None을 반환합니다.
#
# 사용 예시:
#     - 홈페이지: 로그인 시 "환영합니다, OOO님", 비로그인 시 "로그인하세요"
#     - 상품 목록: 누구나 볼 수 있지만, 로그인 사용자에게는 추가 정보 표시
# =============================================================================


async def get_current_user_optional(
    db: DbSession,
    token: Annotated[Optional[str], Depends(get_token_from_cookie)],
) -> Optional[User]:
    """
    현재 사용자 조회 (선택적)

    인증이 필수가 아닌 엔드포인트에서 사용합니다.
    토큰이 없거나 유효하지 않으면 에러 대신 None을 반환합니다.

    Args:
        db: 데이터베이스 세션
        token: JWT 액세스 토큰 (없을 수 있음)

    Returns:
        인증된 User 객체 또는 None

    사용 예시:
        @app.get("/")
        async def home(user: CurrentUserOptional):
            if user:
                return {"message": f"환영합니다, {user.username}님!"}
            return {"message": "로그인하시면 더 많은 기능을 이용할 수 있습니다."}
    """
    # 토큰이 없으면 None 반환 (에러 발생 X)
    if not token:
        return None

    # 토큰이 유효하지 않으면 None 반환
    payload = verify_token(token, token_type="access")
    if not payload:
        return None

    # 사용자 조회
    user_id = int(payload["sub"])
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    # 사용자가 없거나 비활성화되었으면 None 반환
    if not user or not user.is_active:
        return None

    return user


# =============================================================================
# 슈퍼유저 확인 의존성
# =============================================================================
# 관리자 전용 엔드포인트에서 사용합니다.
# 일반 사용자가 접근하면 403 Forbidden 에러를 발생시킵니다.
#
# 의존성 체이닝:
#     get_current_superuser → get_current_user → get_token_from_cookie
#     (슈퍼유저 확인)      → (사용자 인증)    → (토큰 추출)
# =============================================================================


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    현재 슈퍼유저 조회

    관리자 권한이 필요한 엔드포인트에서 사용합니다.
    먼저 일반 인증을 수행한 후, 슈퍼유저 여부를 확인합니다.

    Args:
        current_user: 현재 인증된 사용자 (get_current_user에서 주입)

    Returns:
        슈퍼유저 권한을 가진 User 객체

    Raises:
        HTTPException 403: 슈퍼유저가 아닌 경우

    사용 예시:
        @app.delete("/users/{user_id}")
        async def delete_user(user_id: int, admin: CurrentSuperuser):
            # 관리자만 다른 사용자를 삭제할 수 있음
            await user_service.delete(user_id)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    return current_user


# =============================================================================
# 타입 별칭 (Type Aliases)
# =============================================================================
# Annotated와 Depends를 조합한 타입 별칭을 정의합니다.
# 이를 사용하면 엔드포인트 함수 시그니처가 깔끔해집니다.
#
# Before (별칭 없이):
#     async def endpoint(user: Annotated[User, Depends(get_current_user)]):
#
# After (별칭 사용):
#     async def endpoint(user: CurrentUser):
# =============================================================================

# 인증 필수: 로그인하지 않으면 401 에러
CurrentUser = Annotated[User, Depends(get_current_user)]

# 인증 선택: 로그인하지 않으면 None
CurrentUserOptional = Annotated[Optional[User], Depends(get_current_user_optional)]

# 관리자 필수: 관리자가 아니면 403 에러
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]


# =============================================================================
# 서비스 의존성
# =============================================================================
# 서비스 레이어 인스턴스를 생성하는 의존성 함수들입니다.
# 각 서비스는 데이터베이스 세션을 주입받아 초기화됩니다.
#
# 서비스 레이어의 역할:
#     - 비즈니스 로직 캡슐화
#     - 데이터베이스 작업 추상화
#     - 트랜잭션 관리
# =============================================================================


def get_user_service(db: DbSession) -> UserService:
    """
    UserService 의존성

    사용자 관련 비즈니스 로직을 처리하는 서비스 인스턴스를 생성합니다.

    사용 예시:
        @app.get("/users")
        async def list_users(service: Annotated[UserService, Depends(get_user_service)]):
            return await service.get_all()
    """
    return UserService(db)


def get_auth_service(db: DbSession) -> AuthService:
    """
    AuthService 의존성

    인증 관련 비즈니스 로직을 처리하는 서비스 인스턴스를 생성합니다.
    로그인, 회원가입, 토큰 갱신 등을 담당합니다.
    """
    return AuthService(db)


def get_item_service(db: DbSession) -> ItemService:
    """
    ItemService 의존성

    아이템 CRUD 작업을 처리하는 서비스 인스턴스를 생성합니다.
    """
    return ItemService(db)
