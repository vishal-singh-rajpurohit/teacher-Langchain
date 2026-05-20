from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "PDF Analyzer API"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    api_prefix: str = "/api/v1"

    pgql_url: str = Field(alias="PGQL_URL")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    allowed_hosts: List[str] = Field(default_factory=lambda: ["*"])

    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800
    create_tables_on_startup: bool = False

    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    access_token_expire_seconds: int = 15 * 60
    refresh_token_expire_seconds: int = 7 * 24 * 60 * 60
    max_upload_bytes: int = 20 * 1024 * 1024

    @field_validator("cors_origins", "allowed_hosts", mode="before")
    @classmethod
    def parse_csv(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in {"prod", "production"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
