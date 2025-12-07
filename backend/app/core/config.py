from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env."""

    groq_api_key: str
    hf_token: str | None = None
    allowed_origins: List[str] = ["http://localhost:5173"]
    chunk_size: int = 2000
    chunk_overlap: int = 200
    collection_name: str = "pdf-chat"
    groq_model: str = "llama-3.1-8b-instant"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
