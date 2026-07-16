Food Delivery Platform (Swiggy/Zomato Inspired)

Overview

A production-grade food delivery platform built with FastAPI,
React, and a microservices architecture. The goal is to
implement real-world backend concepts including authentication,
event-driven communication, caching, background jobs, real-time updates,
containerization, observability, and cloud deployment.


food-delivery-platform/
│
├── frontend/
│
├── gateway/
│
├── services/
│   ├── identity-service/
│   ├── catalog-service/
│   ├── order-service/
│   └── delivery-service/
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   ├── monitoring/
│   └── k8s/
│
├── docs/
│
├── .gitignore
│
├── docker-compose.yml
│
└── README.md


main.py
    │
    ▼
router.py
    │
    ▼
health.py

Not
health.py
↓
main.py


Uvicorn

↓

Imports app.main

↓

Creates FastAPI App

↓

Loads Settings

↓

Includes Routers

↓

Starts HTTP Server

↓

Waiting for Requests

Now request comes.

GET /health

↓

FastAPI Routing Table

↓

health.py

↓

Return JSON


Why do we create the SQLAlchemy Engine only once?

A strong answer is:

"The Engine is a heavyweight object that manages the connection pool and database configuration. Creating multiple engines results in multiple connection pools, increased memory usage, inconsistent configuration, and can quickly exhaust the database's connection limit. Therefore, we create a single Engine during application startup and share it across the application."


Phase 1 – Foundation
✅ FastAPI app
✅ Configuration
✅ Health endpoint
✅ Dependency Injection
⏳ Logging
⏳ Exception handling
Phase 2 – Database
SQLAlchemy Engine
Session
Alembic
User model
Phase 3 – Authentication
Signup
Login
JWT
Refresh Tokens
Password hashing
Phase 4 – Production
Docker
PostgreSQL
Redis
Kafka
Unit tests
Integration tests


app/

api/
    auth.py

schemas/
    user.py

repositories/
    user_repository.py

services/
    auth_service.py

models/
    user.py



generate: alembic revision --autogenerate -m "create refresh tokens table"
run: alembic upgrade head