"""
Stora Backend – FastAPI Application Entry Point
================================================

This module creates the FastAPI application instance, wires up routers
and middleware, and exposes a startup event that runs Alembic
migrations automatically on launch.

Run locally with:
    uvicorn app.main:app --reload

Or via Docker:
    docker compose up --build
"""

import subprocess
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import api_router


def _run_migrations() -> None:
    """
    Execute Alembic migrations up to the latest revision.

    Called during application startup to ensure the database schema is
    always up-to-date.  Runs as a subprocess so that the async event
    loop used by Alembic's ``env.py`` does not conflict with the
    already-running FastAPI event loop.
    """
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Alembic migration failed:\n{result.stderr}"
        )


# ── Lifespan (startup / shutdown) ───────────────────────────
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Application lifespan handler.

    On startup:  run Alembic migrations to bring the DB to the latest
                 revision.
    On shutdown: nothing special (engine cleanup is handled elsewhere).
    """
    _run_migrations()
    yield


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
