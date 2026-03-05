# Stora – SaaS E-Commerce & Appointment Platform

A multi-tenant backend built with **FastAPI**, **SQLAlchemy** (async), and **PostgreSQL**.
Managed with [**uv**](https://docs.astral.sh/uv/) for fast, reproducible dependency management.

---

## Features

- **Multi-tenant architecture** – each business (tenant) has isolated data.
- **JWT authentication** – register / login endpoints with bcrypt password hashing.
- **Full CRUD** for all entities: Users, Tenants, Plans, Memberships, Invitations, Products, Combo Items, Orders, Appointments.
- **Pydantic v2 schemas** for strict request validation and clean responses.
- **Async everywhere** – async SQLAlchemy engine + asyncpg driver.
- **Alembic migrations** – auto-run on startup; schema versioning for safe deployments.
- **Environment switching** – toggle between `local` and `production` via `APP_ENV`.
- **Dockerised** – Dockerfile for the backend + docker-compose for backend + Postgres.
- **Test suite** – 45 tests covering auth, CRUD, and health check (pytest + httpx + aiosqlite).
- **CI pipeline** – GitHub Actions workflow for linting, testing, and Docker build.
- **Interactive docs** – Swagger UI at `/docs`, ReDoc at `/redoc`.

---

## Project Structure

```
stora/
├── .github/workflows/ci.yml    # GitHub Actions CI pipeline
├── docker-compose.yml          # Orchestrates backend + Postgres
├── stora-backend/
│   ├── Dockerfile              # Multi-stage image with uv
│   ├── pyproject.toml          # Project metadata & dependencies
│   ├── uv.lock                 # Lockfile (reproducible installs)
│   ├── .env.example            # Environment variable template
│   ├── alembic.ini             # Alembic configuration
│   ├── diagram.md              # ER diagram (Mermaid)
│   ├── alembic/                # Database migrations
│   │   ├── env.py              # Async migration runner
│   │   └── versions/           # Migration scripts
│   ├── tests/                  # Test suite
│   │   ├── conftest.py         # Shared fixtures (in-memory SQLite)
│   │   ├── test_auth.py        # Auth endpoint tests
│   │   ├── test_health.py      # Health check tests
│   │   ├── test_users.py       # User CRUD tests
│   │   ├── test_plans.py       # Plan CRUD tests
│   │   ├── test_tenants.py     # Tenant CRUD tests
│   │   ├── test_products.py    # Product CRUD tests
│   │   ├── test_invitations.py # Invitation CRUD tests
│   │   └── test_memberships_orders.py  # Membership & Order tests
│   └── app/
│       ├── main.py             # FastAPI application entry point
│       ├── config.py           # Settings loaded from env vars
│       ├── database.py         # Async engine, session, Base
│       ├── auth/
│       │   ├── security.py     # Password hashing & JWT utils
│       │   └── dependencies.py # get_current_user dependency
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic request / response schemas
│       ├── crud/               # Database query helpers
│       └── routers/            # API endpoint routers
```

---

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or Docker

### 1. Clone & configure

```bash
git clone https://github.com/ManasesLovera/stora.git
cd stora
cp stora-backend/.env.example stora-backend/.env
# Edit stora-backend/.env as needed
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000**.

| URL                  | Description         |
| -------------------- | ------------------- |
| `GET /health`        | Health check        |
| `GET /docs`          | Swagger UI          |
| `GET /redoc`         | ReDoc               |
| `POST /api/v1/auth/register` | Register    |
| `POST /api/v1/auth/login`    | Login       |

### 3. Run locally (without Docker)

```bash
cd stora-backend
uv sync                   # Install all dependencies (incl. dev)

# Make sure Postgres is running and .env points to it
# (set POSTGRES_HOST=localhost if running Postgres on the host)
uv run uvicorn app.main:app --reload
```

---

## Environment Variables

| Variable                       | Default                | Description                            |
| ------------------------------ | ---------------------- | -------------------------------------- |
| `APP_ENV`                      | `local`                | `local` or `production`                |
| `POSTGRES_USER`                | `stora_user`           | PostgreSQL username                    |
| `POSTGRES_PASSWORD`            | `stora_password`       | PostgreSQL password                    |
| `POSTGRES_DB`                  | `stora_db`             | PostgreSQL database name               |
| `POSTGRES_HOST`                | `db`                   | Hostname (use `db` in Docker)          |
| `POSTGRES_PORT`                | `5432`                 | PostgreSQL port                        |
| `DATABASE_URL`                 | *(assembled)*          | Full URL – overrides individual params |
| `SECRET_KEY`                   | `change-me-...`        | JWT signing key                        |
| `ALGORITHM`                    | `HS256`                | JWT algorithm                          |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | `30`                   | Token lifetime in minutes              |

---

## API Endpoints Overview

All business endpoints live under `/api/v1`. Protected endpoints require a `Bearer <token>` header.

| Method   | Path                                    | Auth | Description                  |
| -------- | --------------------------------------- | ---- | ---------------------------- |
| `POST`   | `/api/v1/auth/register`                 | No   | Register a new user          |
| `POST`   | `/api/v1/auth/login`                    | No   | Login and get JWT            |
| `GET`    | `/api/v1/users/me`                      | Yes  | Current user profile         |
| `GET`    | `/api/v1/users/`                        | Yes  | List users                   |
| `GET`    | `/api/v1/users/{id}`                    | Yes  | Get user by ID               |
| `PATCH`  | `/api/v1/users/{id}`                    | Yes  | Update user                  |
| `DELETE` | `/api/v1/users/{id}`                    | Yes  | Delete user                  |
| `GET`    | `/api/v1/plans/`                        | No   | List plans                   |
| `GET`    | `/api/v1/plans/{id}`                    | No   | Get plan                     |
| `POST`   | `/api/v1/plans/`                        | Yes  | Create plan                  |
| `PATCH`  | `/api/v1/plans/{id}`                    | Yes  | Update plan                  |
| `DELETE` | `/api/v1/plans/{id}`                    | Yes  | Delete plan                  |
| `GET`    | `/api/v1/tenants/`                      | Yes  | List tenants                 |
| `GET`    | `/api/v1/tenants/{id}`                  | Yes  | Get tenant                   |
| `POST`   | `/api/v1/tenants/`                      | Yes  | Create tenant                |
| `PATCH`  | `/api/v1/tenants/{id}`                  | Yes  | Update tenant                |
| `DELETE` | `/api/v1/tenants/{id}`                  | Yes  | Delete tenant                |
| `GET`    | `/api/v1/memberships/tenant/{id}`       | Yes  | List memberships by tenant   |
| `GET`    | `/api/v1/memberships/{id}`              | Yes  | Get membership               |
| `POST`   | `/api/v1/memberships/`                  | Yes  | Create membership            |
| `PATCH`  | `/api/v1/memberships/{id}`              | Yes  | Update membership            |
| `DELETE` | `/api/v1/memberships/{id}`              | Yes  | Delete membership            |
| `GET`    | `/api/v1/invitations/tenant/{id}`       | Yes  | List invitations by tenant   |
| `GET`    | `/api/v1/invitations/{id}`              | Yes  | Get invitation               |
| `GET`    | `/api/v1/invitations/token/{token}`     | No   | Get invitation by token      |
| `POST`   | `/api/v1/invitations/`                  | Yes  | Create invitation            |
| `DELETE` | `/api/v1/invitations/{id}`              | Yes  | Delete invitation            |
| `GET`    | `/api/v1/products/tenant/{id}`          | Yes  | List products by tenant      |
| `GET`    | `/api/v1/products/{id}`                 | Yes  | Get product                  |
| `POST`   | `/api/v1/products/`                     | Yes  | Create product               |
| `PATCH`  | `/api/v1/products/{id}`                 | Yes  | Update product               |
| `DELETE` | `/api/v1/products/{id}`                 | Yes  | Delete product               |
| `GET`    | `/api/v1/combo-items/product/{id}`      | Yes  | List combo items by product  |
| `GET`    | `/api/v1/combo-items/{id}`              | Yes  | Get combo item               |
| `POST`   | `/api/v1/combo-items/`                  | Yes  | Create combo item            |
| `PATCH`  | `/api/v1/combo-items/{id}`              | Yes  | Update combo item            |
| `DELETE` | `/api/v1/combo-items/{id}`              | Yes  | Delete combo item            |
| `GET`    | `/api/v1/orders/tenant/{id}`            | Yes  | List orders by tenant        |
| `GET`    | `/api/v1/orders/{id}`                   | Yes  | Get order                    |
| `POST`   | `/api/v1/orders/`                       | Yes  | Create order                 |
| `PATCH`  | `/api/v1/orders/{id}`                   | Yes  | Update order                 |
| `DELETE` | `/api/v1/orders/{id}`                   | Yes  | Delete order                 |
| `GET`    | `/api/v1/appointments/tenant/{id}`      | Yes  | List appointments by tenant  |
| `GET`    | `/api/v1/appointments/{id}`             | Yes  | Get appointment              |
| `POST`   | `/api/v1/appointments/`                 | Yes  | Create appointment           |
| `PATCH`  | `/api/v1/appointments/{id}`             | Yes  | Update appointment           |
| `DELETE` | `/api/v1/appointments/{id}`             | Yes  | Delete appointment           |

---

## Conventions & Patterns

- **Layered architecture**: `routers → crud → models` with Pydantic schemas at the boundary.
- **Dependency injection**: database sessions and authentication via FastAPI `Depends`.
- **Async/await**: all database operations use `AsyncSession`.
- **UUID primary keys**: every entity uses `uuid4` for IDs.
- **Environment-based config**: `pydantic-settings` loads from `.env` with sensible defaults.
- **Alembic migrations**: schema changes are versioned; migrations auto-run on startup.
- **Well-commented code**: every module, class, function, and column has docstrings/comments.

---

## Database Migrations

Migrations are managed with **Alembic** and run automatically when the application starts.

```bash
cd stora-backend

# Generate a new migration after model changes
uv run alembic revision --autogenerate -m "description_of_change"

# Apply migrations manually
uv run alembic upgrade head

# Downgrade one revision
uv run alembic downgrade -1
```

---

## Testing

The test suite uses **pytest** with **pytest-asyncio** and an **in-memory SQLite** database (no PostgreSQL required).

```bash
cd stora-backend

# Run all tests
uv run pytest tests/ -v

# Run a specific test file
uv run pytest tests/test_auth.py -v

# Run with coverage (install pytest-cov first)
uv run pytest tests/ --cov=app --cov-report=term-missing
```

### Test structure

| File                             | Tests | Coverage                                 |
| -------------------------------- | ----- | ---------------------------------------- |
| `test_health.py`                 | 1     | Health check endpoint                    |
| `test_auth.py`                   | 10    | Register, login, token validation        |
| `test_users.py`                  | 5     | User CRUD operations                     |
| `test_plans.py`                  | 6     | Plan CRUD operations                     |
| `test_tenants.py`                | 6     | Tenant CRUD operations                   |
| `test_products.py`               | 5     | Product CRUD operations                  |
| `test_invitations.py`            | 4     | Invitation CRUD operations               |
| `test_memberships_orders.py`     | 8     | Membership & Order CRUD operations       |

---

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and PR to `main`:

1. **Lint** – Checks code style with `ruff check` and `ruff format` (via uv).
2. **Test** – Runs the full pytest suite (45 tests) with in-memory SQLite (via uv).
3. **Build** – Builds the Docker image to verify the Dockerfile.

---

## License

This project is private. All rights reserved.
