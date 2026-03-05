# Stora – SaaS E-Commerce & Appointment Platform

A multi-tenant backend built with **FastAPI**, **SQLAlchemy** (async), and **PostgreSQL**.

---

## Features

- **Multi-tenant architecture** – each business (tenant) has isolated data.
- **JWT authentication** – register / login endpoints with bcrypt password hashing.
- **Full CRUD** for all entities: Users, Tenants, Plans, Memberships, Invitations, Products, Combo Items, Orders, Appointments.
- **Pydantic v2 schemas** for strict request validation and clean responses.
- **Async everywhere** – async SQLAlchemy engine + asyncpg driver.
- **Environment switching** – toggle between `local` and `production` via `APP_ENV`.
- **Dockerised** – Dockerfile for the backend + docker-compose for backend + Postgres.
- **Interactive docs** – Swagger UI at `/docs`, ReDoc at `/redoc`.

---

## Project Structure

```
stora/
├── docker-compose.yml          # Orchestrates backend + Postgres
├── stora-backend/
│   ├── Dockerfile              # Multi-stage Python image
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variable template
│   ├── diagram.md              # ER diagram (Mermaid)
│   └── app/
│       ├── main.py             # FastAPI application entry point
│       ├── config.py           # Settings loaded from env vars
│       ├── database.py         # Async engine, session, Base
│       ├── auth/
│       │   ├── security.py     # Password hashing & JWT utils
│       │   └── dependencies.py # get_current_user dependency
│       ├── models/             # SQLAlchemy ORM models
│       │   ├── user.py
│       │   ├── tenant.py
│       │   ├── plan.py
│       │   ├── membership.py
│       │   ├── invitation.py
│       │   ├── product.py
│       │   ├── combo_item.py
│       │   ├── order.py
│       │   └── appointment.py
│       ├── schemas/            # Pydantic request / response schemas
│       │   ├── user.py
│       │   ├── tenant.py
│       │   ├── plan.py
│       │   ├── membership.py
│       │   ├── invitation.py
│       │   ├── product.py
│       │   ├── combo_item.py
│       │   ├── order.py
│       │   ├── appointment.py
│       │   └── auth.py
│       ├── crud/               # Database query helpers
│       │   ├── user.py
│       │   ├── tenant.py
│       │   ├── plan.py
│       │   ├── membership.py
│       │   ├── invitation.py
│       │   ├── product.py
│       │   ├── combo_item.py
│       │   ├── order.py
│       │   └── appointment.py
│       └── routers/            # API endpoint routers
│           ├── auth.py
│           ├── users.py
│           ├── tenants.py
│           ├── plans.py
│           ├── memberships.py
│           ├── invitations.py
│           ├── products.py
│           ├── combo_items.py
│           ├── orders.py
│           └── appointments.py
```

---

## Quick Start

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
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Make sure Postgres is running and .env points to it
# (set POSTGRES_HOST=localhost if running Postgres on the host)
uvicorn app.main:app --reload
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
- **Well-commented code**: every module, class, function, and column has docstrings/comments.

---

## License

This project is private. All rights reserved.
