"""
Shared test fixtures for the Stora backend test suite.

Uses an in-memory SQLite database (via aiosqlite) so tests run fast
and do not require a running PostgreSQL instance.  A fresh database
is created for **every test function** to guarantee isolation.
"""

from collections.abc import AsyncGenerator
from unittest.mock import patch

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import Settings, get_settings
from app.database import Base, get_db
from app.main import app

# ── Test-specific settings override ─────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


def get_test_settings() -> Settings:
    """Return settings configured for the test environment."""
    return Settings(
        app_env="test",
        database_url=TEST_DATABASE_URL,
        secret_key="test-secret-key",
        postgres_host="localhost",
    )


# ── Fixtures ─────────────────────────────────────────────────


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a clean async database session backed by in-memory SQLite.

    Creates all tables before the test and drops them afterwards so
    every test starts with a blank database.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide an HTTP test client wired to the FastAPI app.

    Overrides ``get_db`` and ``get_settings`` so the app uses the
    in-memory test database and test configuration.  Also patches
    ``_run_migrations`` so Alembic is not invoked during tests
    (tables are already created by the ``db_session`` fixture).
    """

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_settings] = get_test_settings

    # Patch Alembic migration call so it is skipped in tests.
    with patch("app.main._run_migrations"):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()
