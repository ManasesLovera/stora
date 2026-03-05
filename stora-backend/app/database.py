"""
Database connection module for the Stora backend.

Creates an async SQLAlchemy engine and session factory.  Every
request-handler that needs database access should depend on
``get_db`` which yields a scoped ``AsyncSession``.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

# ── Engine & session factory ─────────────────────────────────
settings = get_settings()

engine = create_async_engine(
    settings.async_database_url,
    echo=(settings.app_env == "local"),  # Log SQL only in local mode
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Declarative base ────────────────────────────────────────
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every model inherits from this class so that ``Base.metadata``
    contains the full schema and can be used for table creation /
    migrations.
    """

    pass


# ── Dependency ───────────────────────────────────────────────
async def get_db():
    """
    FastAPI dependency that provides a database session.

    Yields an ``AsyncSession`` and guarantees it is closed after the
    request finishes, even if an exception occurs.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
