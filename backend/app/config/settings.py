"""
Curio AI — Application Settings (env-based via Pydantic Settings).

All configuration is loaded from environment variables or .env file.
Use get_settings() to access the cached singleton.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Environment ──────────────────────────────────────────────
    ENV: str = Field(default="dev", description="Environment: dev | staging | prod")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    DEBUG: bool = Field(default=True, description="Debug mode flag")

    # ── AI Provider ──────────────────────────────────────────────
    AI_PROVIDER: str = Field(
        default="mock",
        description="AI provider to use: mock | openai | gemini | groq | local",
    )
    AI_MODEL: str = Field(
        default="mock-v1",
        description="Model identifier for the chosen AI provider",
    )
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key (required when AI_PROVIDER=openai)",
    )
    GEMINI_API_KEY: Optional[str] = Field(
        default=None,
        description="Google Gemini API key (required when AI_PROVIDER=gemini)",
    )
    GROQ_API_KEY: Optional[str] = Field(
        default=None,
        description="Groq API key (required when AI_PROVIDER=groq)",
    )
    ENABLE_BACKEND_TTS: bool = Field(
        default=False,
        description="Set to True to use OpenAI TTS for backend audio generation",
    )

    # ── Session ──────────────────────────────────────────────────
    SESSION_TTL_MINUTES: int = Field(
        default=60,
        description="Session time-to-live in minutes before expiry",
    )

    # ── Server / CORS ────────────────────────────────────────────
    HOST: str = Field(default="0.0.0.0", description="Server bind host")
    PORT: int = Field(default=8000, description="Server bind port")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"],
        description="Allowed CORS origins",
    )

    # ── Rate Limiting (placeholders for future) ──────────────────
    RATE_LIMIT_ENABLED: bool = Field(default=False, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(
        default=60,
        description="Max requests per minute per client",
    )

    # ── Future: Database ─────────────────────────────────────────
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Database connection string (future use)",
    )
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection string (future use)",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }

    def safe_dict(self) -> dict:
        """Return settings as dict with secrets masked."""
        data = self.model_dump()
        secret_keys = {"OPENAI_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "DATABASE_URL", "REDIS_URL"}
        for key in secret_keys:
            if data.get(key):
                data[key] = "***REDACTED***"
        return data


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings singleton."""
    return Settings()
