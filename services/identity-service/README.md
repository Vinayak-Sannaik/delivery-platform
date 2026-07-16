# Identity Service

Identity Service is responsible for authentication and authorization for the Food Delivery Platform. It provides secure user registration, login, JWT-based authentication, and serves as the central identity provider for all platform services.

## 🚀 Live Demo

**API Documentation (Swagger UI)**

https://delivery-platform-xo8w.onrender.com/docs#/Authentication/login_auth_login_post

---

## Features

- User Registration
- User Login
- JWT Access Token Authentication
- Refresh Token Support
- Password Hashing
- Input Validation
- Alembic Database Migrations
- Layered Architecture (Router → Service → Repository)
- Dockerized Application
- Hosted on Render
- PostgreSQL (Supabase)

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy
- Alembic
- Pydantic
- JWT
- Docker
- Render

---

## Project Structure

```text
app/
├── core/              # Application configuration
├── db/                # Database session and base models
├── dependencies/      # FastAPI dependency injection
├── models/            # SQLAlchemy models
├── repositories/      # Database access layer
├── routers/           # API endpoints
├── schemas/           # Request/Response models
├── security/          # Password hashing and JWT
├── services/          # Business logic
├── main.py            # FastAPI application entry point

alembic/
Dockerfile
docker-compose.yml
requirements.txt
.env.example
README.md
```

---

## Architecture

```text
                HTTP Request
                     │
                     ▼
                FastAPI Router
                     │
                     ▼
                Service Layer
                     │
                     ▼
              Repository Layer
                     │
                     ▼
             PostgreSQL Database
```

### Responsibilities

- **Router** → Handles HTTP requests and responses.
- **Service** → Contains business logic and transaction management.
- **Repository** → Performs database operations.
- **Model** → Database table definitions.
- **Schema** → Request validation and response serialization.
- **Security** → Password hashing and JWT generation/verification.
- **Dependencies** → Provides shared dependencies such as database sessions and services.

---

# Getting Started

## Clone the repository

```bash
git clone <repository-url>
cd food-delivery-platform/services/identity-service
```

---

# Running with Docker (Recommended)

```bash
docker compose up --build
```

Swagger UI

```
http://localhost:8000/docs
```

---

# Running Locally

## Create a virtual environment

```bash
python -m venv .venv
```

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:5432/<database>

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```

---

## Database Migrations

Create migration

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations

```bash
alembic upgrade head
```

Rollback last migration

```bash
alembic downgrade -1
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Application

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and receive JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/users/me` | Get authenticated user |

---

# Deployment

- Dockerized using Docker Compose
- Hosted on Render
- PostgreSQL hosted on Supabase

---

# Future Improvements

- Role-Based Access Control (RBAC)
- OAuth (Google/GitHub Login)
- Email Verification
- Password Reset
- Audit Logging
- Rate Limiting
- Multi-Factor Authentication (MFA)

---