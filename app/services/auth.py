"""
Auth Service (인증 서비스)
인증 관련 비즈니스 로직

=============================================================================
JWT (JSON Web Token) 인증이란?
=============================================================================
JWT는 사용자 인증 정보를 JSON 형식으로 인코딩한 토큰입니다.
서버가 세션을 저장하지 않아도 되므로 확장성이 좋습니다.

JWT 구조 (점으로 구분된 3개 파트):
    Header.Payload.Signature

    1. Header (헤더): 토큰 타입(JWT)과 해싱 알고리즘(HS256)
       예: {"alg": "HS256", "typ": "JWT"}

    2. Payload (페이로드): 실제 데이터 (클레임)
       예: {"sub": "123", "exp": 1234567890, "type": "access"}
       - sub: 주체 (사용자 ID)
       - exp: 만료 시간
       - type: 토큰 종류 (access/refresh)

    3. Signature (서명): Header + Payload를 비밀키로 서명
       서명을 통해 토큰 변조 여부를 검증합니다.

인증 흐름:
    1. 로그인 성공 → 서버가 JWT 생성 → 쿠키에 저장
    2. 이후 요청 → 브라우저가 쿠키 자동 전송 → 서버가 JWT 검증
    3. 토큰 만료 → 리프레시 토큰으로 새 토큰 발급

Access Token vs Refresh Token:
    - Access Token: 짧은 수명 (15분~1시간), API 접근용
    - Refresh Token: 긴 수명 (7일~30일), 새 Access Token 발급용

    왜 2개의 토큰을 사용하나요?
    - Access Token이 탈취되어도 짧은 시간만 유효
    - Refresh Token은 자주 사용하지 않아 탈취 위험 낮음
=============================================================================
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, ConflictError, ValidationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.models.user import User
from app.schemas.user import Token, UserCreate
from app.services.user import UserService


class AuthService:
    """
    인증 서비스

    사용자 인증과 관련된 모든 비즈니스 로직을 담당합니다:
    - 회원가입 (register)
    - 로그인 (login)
    - 토큰 갱신 (refresh_tokens)
    - 비밀번호 변경 (change_password)

    서비스 레이어의 역할:
        - 컨트롤러(라우터)와 데이터 레이어(모델) 사이의 중간 계층
        - 비즈니스 로직을 캡슐화하여 재사용 가능하게 함
        - 테스트하기 쉬운 구조 제공

    사용 예시:
        auth_service = AuthService(db_session)
        token = await auth_service.login(email, password)
    """

    def __init__(self, db: AsyncSession):
        """
        AuthService 초기화

        Args:
            db: SQLAlchemy 비동기 데이터베이스 세션
                - 요청마다 새로운 세션이 생성됨
                - 서비스 내 모든 DB 작업이 같은 세션을 공유
                - 트랜잭션 일관성 보장
        """
        self.db = db
        # UserService를 조합(composition)하여 사용자 관련 기능 재사용
        self.user_service = UserService(db)

    # =========================================================================
    # 회원가입
    # =========================================================================

    async def register(self, user_in: UserCreate) -> User:
        """
        회원가입 처리

        새로운 사용자를 등록합니다. 이메일과 사용자명의 중복을 확인하고,
        비밀번호를 해시화하여 저장합니다.

        Args:
            user_in: 사용자 생성 데이터
                - email: 이메일 주소 (고유)
                - username: 사용자명 (고유)
                - password: 평문 비밀번호 (해시화되어 저장됨)
                - full_name: 이름 (선택)

        Returns:
            생성된 User 객체 (비밀번호 제외)

        Raises:
            ConflictError: 이메일 또는 사용자명이 이미 존재할 경우

        회원가입 흐름:
            1. 이메일 중복 확인
            2. 사용자명 중복 확인
            3. 비밀번호 해시화 (bcrypt)
            4. DB에 사용자 저장
            5. 생성된 사용자 반환

        보안 고려사항:
            - 비밀번호는 절대 평문으로 저장하지 않음
            - bcrypt 해시 사용 (salt 자동 포함)
            - 같은 비밀번호도 매번 다른 해시값 생성
        """
        # Step 1: 이메일 중복 확인
        # 이미 등록된 이메일이면 회원가입 불가
        if await self.user_service.is_email_taken(user_in.email):
            raise ConflictError("이미 등록된 이메일입니다.")

        # Step 2: 사용자명 중복 확인
        # 사용자명은 로그인이나 프로필 URL에 사용될 수 있음
        if await self.user_service.is_username_taken(user_in.username):
            raise ConflictError("이미 사용중인 사용자명입니다.")

        # Step 3: 사용자 생성 (UserService에서 비밀번호 해시화 처리)
        user = await self.user_service.create(user_in)
        return user

    # =========================================================================
    # 로그인
    # =========================================================================

    async def login(self, email: str, password: str) -> Token:
        """
        로그인 처리

        이메일과 비밀번호를 검증하고, 인증 토큰을 발급합니다.

        Args:
            email: 사용자 이메일
            password: 평문 비밀번호

        Returns:
            Token: JWT 토큰 쌍
                - access_token: API 접근용 (짧은 수명)
                - refresh_token: 토큰 갱신용 (긴 수명)

        Raises:
            AuthenticationError: 다음 경우에 발생
                - 이메일이 존재하지 않음
                - 비밀번호가 틀림
                - 계정이 비활성화됨

        로그인 흐름:
            1. 이메일로 사용자 조회
            2. 비밀번호 검증 (bcrypt)
            3. 계정 활성 상태 확인
            4. Access Token 생성
            5. Refresh Token 생성
            6. 토큰 반환

        보안 고려사항:
            - 이메일 존재 여부와 비밀번호 오류를 구분하지 않음
              (공격자가 유효한 이메일을 알아내는 것을 방지)
            - 비밀번호는 해시 비교로만 검증 (평문 비교 X)
        """
        # Step 1: 이메일로 사용자 조회
        user = await self.user_service.get_by_email(email)
        if not user:
            # 보안: "이메일이 존재하지 않음"이라고 구체적으로 알리지 않음
            raise AuthenticationError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # Step 2: 비밀번호 검증
        # verify_password: 입력된 평문 비밀번호와 저장된 해시를 비교
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # Step 3: 계정 활성 상태 확인
        # 관리자가 계정을 비활성화했을 수 있음
        if not user.is_active:
            raise AuthenticationError("비활성화된 계정입니다.")

        # Step 4 & 5: JWT 토큰 생성
        # subject에 사용자 ID를 포함하여 나중에 사용자를 식별
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        # Step 6: 토큰 반환
        # 이 토큰들은 라우터에서 httpOnly 쿠키로 설정됨
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    # =========================================================================
    # 토큰 갱신
    # =========================================================================

    async def refresh_tokens(self, refresh_token: str) -> Token:
        """
        토큰 갱신

        Refresh Token을 사용하여 새로운 토큰 쌍을 발급합니다.
        Access Token이 만료되었을 때 사용합니다.

        Args:
            refresh_token: 기존 Refresh Token

        Returns:
            Token: 새로운 JWT 토큰 쌍
                - access_token: 새 Access Token
                - refresh_token: 새 Refresh Token (토큰 로테이션)

        Raises:
            AuthenticationError: 다음 경우에 발생
                - Refresh Token이 유효하지 않음
                - Refresh Token이 만료됨
                - 사용자가 존재하지 않음
                - 계정이 비활성화됨

        토큰 갱신 흐름:
            1. Refresh Token 검증 (서명, 만료시간, 타입)
            2. 토큰에서 사용자 ID 추출
            3. 사용자 조회 및 상태 확인
            4. 새 토큰 쌍 생성
            5. 새 토큰 반환

        토큰 로테이션 (Token Rotation):
            Refresh Token도 매번 새로 발급합니다.
            - 장점: 한 번 사용된 Refresh Token은 무효화되어 보안 강화
            - 단점: 동시 요청 시 문제 발생 가능 (경쟁 조건)

        사용 시나리오:
            1. 클라이언트가 API 요청
            2. 서버가 401 응답 (Access Token 만료)
            3. 클라이언트가 /refresh 엔드포인트 호출
            4. 새 토큰으로 원래 요청 재시도
        """
        # Step 1: Refresh Token 검증
        # token_type="refresh"로 Access Token을 잘못 사용하는 것 방지
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise AuthenticationError("유효하지 않은 토큰입니다.")

        # Step 2: 페이로드에서 사용자 ID 추출
        # JWT의 'sub' (subject) 클레임에 저장된 사용자 ID
        user_id = int(payload["sub"])

        # Step 3: 사용자 조회 및 상태 확인
        user = await self.user_service.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("사용자를 찾을 수 없거나 비활성화된 계정입니다.")

        # Step 4 & 5: 새 토큰 쌍 생성 및 반환
        new_access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    # =========================================================================
    # 현재 사용자 조회
    # =========================================================================

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        현재 사용자 조회

        JWT Access Token에서 사용자 정보를 추출합니다.

        Args:
            token: JWT Access Token

        Returns:
            인증된 User 객체 또는 None

        Note:
            이 메서드는 예외를 발생시키지 않고 None을 반환합니다.
            예외 처리가 필요한 경우 deps.py의 get_current_user를 사용하세요.
        """
        # 토큰 검증
        payload = verify_token(token, token_type="access")
        if not payload:
            return None

        # 사용자 조회
        user_id = int(payload["sub"])
        user = await self.user_service.get_by_id(user_id)

        # 사용자 상태 확인
        if not user or not user.is_active:
            return None

        return user

    # =========================================================================
    # 비밀번호 변경
    # =========================================================================

    async def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> User:
        """
        비밀번호 변경

        현재 비밀번호를 확인한 후 새 비밀번호로 변경합니다.

        Args:
            user: 현재 로그인한 사용자 객체
            current_password: 현재 비밀번호 (검증용)
            new_password: 새 비밀번호

        Returns:
            수정된 User 객체

        Raises:
            ValidationError: 현재 비밀번호가 틀린 경우

        보안 고려사항:
            - 현재 비밀번호 확인 필수 (세션 탈취 공격 방지)
            - 새 비밀번호는 bcrypt로 해시화
            - 비밀번호 변경 시 기존 세션/토큰 무효화 고려 필요
              (이 보일러플레이트에서는 구현하지 않음)
        """
        # Step 1: 현재 비밀번호 검증
        # 다른 사람이 로그인된 세션을 탈취해도
        # 현재 비밀번호를 모르면 변경 불가
        if not verify_password(current_password, user.hashed_password):
            raise ValidationError("현재 비밀번호가 올바르지 않습니다.")

        # Step 2: 새 비밀번호 해시화 및 저장
        user.hashed_password = get_password_hash(new_password)

        # Step 3: DB에 변경사항 반영
        # flush: 변경사항을 DB에 전송 (아직 커밋은 아님)
        # refresh: DB에서 최신 데이터로 객체 갱신
        await self.db.flush()
        await self.db.refresh(user)

        return user
