"""
Application Configuration

환경 변수를 통한 애플리케이션 설정 관리
Pydantic Settings를 사용하여 타입 안전성과 유효성 검사 제공
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App Settings
    app_name: str = "FastAPI-HTMX-Boilerplate"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-in-production"

    # Database
    database_url: str = "sqlite+aiosqlite:///./app.db"

    # JWT Settings
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 7

    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True
    workers: int = 1

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Logging
    log_level: str = "INFO"

    # Redis (Optional)
    redis_url: Optional[str] = None

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """CORS origins 문자열을 리스트로 변환"""
        if isinstance(v, str):
            import json

            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_development(self) -> bool:
        """개발 환경 여부"""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """운영 환경 여부"""
        return self.app_env == "production"

    @property
    def is_testing(self) -> bool:
        """테스트 환경 여부"""
        return self.app_env == "testing"


@lru_cache
def get_settings() -> Settings:
    """설정 인스턴스 반환 (캐싱됨)"""
    return Settings()


settings = get_settings()
