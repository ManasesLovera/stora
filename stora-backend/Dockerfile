# ──────────────────────────────────────────────────────────────
# Stora Backend – Dockerfile
#
# Uses uv for fast, reproducible dependency installation.
#
# Multi-stage build:
#   1. Install Python dependencies in a builder stage with uv.
#   2. Copy only the installed packages into the final slim image.
# ──────────────────────────────────────────────────────────────

# ── Stage 1: Builder ─────────────────────────────────────────
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /build

# Install build dependencies required by some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency manifests first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install production dependencies only (no dev group)
RUN uv sync --frozen --no-dev --no-install-project

# ── Stage 2: Runtime ─────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Install only the runtime PostgreSQL client library
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from builder
COPY --from=builder /build/.venv /app/.venv

# Put the venv on PATH so python/uvicorn are found without activation
ENV PATH="/app/.venv/bin:$PATH"

# Copy application source code
COPY . .

# Expose the default Uvicorn port
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
