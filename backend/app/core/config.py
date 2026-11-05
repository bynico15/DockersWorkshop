from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevOps Workshop API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    environment: str = "development"
    allowed_origins: list[str] = ["http://localhost:5173"]
    database_path: str = "data/catalog.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
