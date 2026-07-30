from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # ==========================================================
    # APPLICATION
    # ==========================================================

    PROJECT_NAME: str = Field(default="Vishwaarpana Havihi")
    API_V1_PREFIX: str = Field(default="/api/v1")

    DEBUG: bool = Field(default=False)

    # ==========================================================
    # DATABASE
    # ==========================================================

    DATABASE_URL: str

    # ==========================================================
    # SECURITY
    # ==========================================================

    SECRET_KEY: str

    ALGORITHM: str = Field(default="HS256")

    JWT_ISSUER: str = Field(
        default="Vishwaarpana-Havihi"
    )

    JWT_AUDIENCE: str = Field(
        default="Vishwaarpana-Havihi-API"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7
    )

    # ==========================================================
    # GOOGLE GEMINI
    # ==========================================================

    GEMINI_API_KEY: str = Field(
        default=""
    )

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash"
    )

    # ==========================================================
    # CORS
    # ==========================================================

    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=[
            "http://localhost:3000",
        ]
    )

    # ==========================================================
    # ENVIRONMENT
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """
    return Settings()


settings = get_settings()