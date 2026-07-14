from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    PROJECT_NAME: str = Field(default="Vishwaarpana Havihi")
    API_V1_PREFIX: str = Field(default="/api/v1")

    DEBUG: bool = Field(default=False)

    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str = Field(default="HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    BACKEND_CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000"])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()