"""
Configuration module for the Stora backend.

Uses pydantic-settings to load environment variables from a .env file
or the system environment.  A single ``Settings`` instance is shared
across the application via the ``get_settings`` helper.

Environment switching
---------------------
Set ``APP_ENV`` to **"local"** (default) or **"production"**.  The
database URL is assembled automatically from the individual Postgres
parameters, but can be overridden entirely via ``DATABASE_URL``.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide settings loaded from environment variables."""

    # ── General ──────────────────────────────────────────────
    app_env: str = "local"
    """Current environment: 'local' or 'production'."""

    # ── PostgreSQL ───────────────────────────────────────────
    postgres_user: str = "stora_user"
    postgres_password: str = "stora_password"
    postgres_db: str = "stora_db"
    postgres_host: str = "db"
    postgres_port: int = 5432

    database_url: str | None = None
    """
    Full database URL.  When *not* provided the URL is assembled from
    the individual ``POSTGRES_*`` variables.
    """

    # ── JWT Authentication ───────────────────────────────────
    secret_key: str = "change-me-to-a-random-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # ── Pydantic-settings configuration ──────────────────────
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def async_database_url(self) -> str:
        """
        Return the async-compatible database URL.

        If ``DATABASE_URL`` is explicitly set it is returned as-is
        (replacing ``postgresql://`` with ``postgresql+asyncpg://`` when
        needed).  Otherwise the URL is built from individual parameters.
        """
        if self.database_url:
            url = self.database_url
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url

        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached ``Settings`` instance.

    Using ``lru_cache`` ensures the .env file is read only once and the
    same object is reused for every call.
    """
    return Settings()
