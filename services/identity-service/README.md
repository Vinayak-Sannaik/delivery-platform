# Identity Service

Identity Service is responsible for authentication and authorization for the Food Delivery Platform.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT

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
- **Dependencies** → Creates and injects shared objects such as database sessions and services.

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd services/identity-service
```
### 2. Docker
```bash
docker compose up
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:5432/<database>

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```

---

## Database Migrations

### Create a migration

```bash
alembic revision --autogenerate -m "migration message"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback the last migration

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

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```