"""
Stora Backend – FastAPI Application Entry Point
================================================

This module creates the FastAPI application instance, wires up routers
and middleware, and exposes a startup event that creates database
tables automatically on first launch.

Run locally with:
    uvicorn app.main:app --reload

Or via Docker:
    docker compose up --build
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers import api_router


# ── Lifespan (startup / shutdown) ───────────────────────────
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Application lifespan handler.

    On startup:  create all database tables that do not yet exist.
    On shutdown: dispose of the async engine connection pool.
    """
    # Create tables (safe to call repeatedly – only creates missing ones)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


# ── Application factory ─────────────────────────────────────
settings = get_settings()

app = FastAPI(
    title="Stora API",
    description=(
        "Backend API for the Stora SaaS e-commerce and appointment "
        "management platform.  Provides multi-tenant CRUD operations, "
        "JWT authentication, product management, order tracking, and "
        "appointment scheduling."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (allow all in local; restrict in production) ────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "local" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount all versioned routes under /api/v1 ─────────────────
app.include_router(api_router, prefix="/api/v1")


# ── Health-check endpoint ────────────────────────────────────
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Returns a simple JSON response to verify the API is running.",
)
async def health_check():
    """Return a basic health-check response."""
    return {"status": "ok", "environment": settings.app_env}
