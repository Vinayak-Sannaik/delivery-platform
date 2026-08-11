# 🍔 Food Delivery Platform

A production-inspired microservices-based Food Delivery Platform built to learn and demonstrate backend engineering concepts such as distributed systems, API Gateway, authentication, asynchronous communication, caching, and containerized deployments.

The project is designed using industry-standard architecture while remaining simple enough to understand and extend.

---

# 🚀 Live Services

| Service | Status | Live |
|----------|--------|------|
| Identity Service | ✅ Live | https://delivery-platform-xo8w.onrender.com/docs |
| Catalog Service | ✅ Live | https://food-catalog-service.onrender.com/docs |
| Order Service | ✅ Live | https://delivery-platform-oezs.onrender.com/docs|
| Delivery Service | ✅ Live | https://delivery-service-nzxj.onrender.com/docs |
| Notification Service | ✅ Live | https://delivery-platform-dzuv.onrender.com/docs |

---

# Architecture

```text
                        Client
                           │
                           ▼
                     API Gateway
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Identity Service     Catalog Service    Order Service
        │                  │                  │
        └──────────────┬───┴──────────────┐
                       ▼                  ▼
                 Supabase PostgreSQL    Redis
                                         │
                                         ▼
                                       Kafka
                                         │
                                         ▼
                                 Delivery Service
```

---

# Repository Structure

```text
food-delivery-platform/
│
├── frontend/                 # React Frontend
│
├── gateway/                  # API Gateway
│
├── services/
│   ├── identity-service/     # Authentication & Authorization
│   ├── catalog-service/      # Restaurants, Menus & Food Items
│   ├── order-service/        # Cart & Orders
│   └── delivery-service/     # Delivery Partner Management
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   ├── monitoring/
│   └── k8s/
│
├── docs/
│
├── docker-compose.yml
│
└── README.md
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- JWT Authentication

## Database

- PostgreSQL (Supabase)

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

## Caching

- Redis *(Planned)*

## Messaging

- Kafka *(Planned)*

## Frontend

- React
- TypeScript

## Infrastructure

- Docker
- Docker Compose
- Render
- GitHub Actions *(Planned)*

---

# Microservices

## ✅ Identity Service

Responsible for:

- User Registration
- Login
- JWT Authentication
- Refresh Tokens
- Password Hashing

Documentation:

```
services/identity-service
```

Live API:

https://delivery-platform-xo8w.onrender.com/docs

---

## 🚧 Catalog Service

Responsible for:

- Restaurants
- Menus
- Food Categories
- Food Items
- Search

Status:

Under Development

---

## 📋 Order Service

Responsible for:

- Shopping Cart
- Order Placement
- Order Status
- Payment Integration

Status:

Planned

---

## 📋 Delivery Service

Responsible for:

- Delivery Partners
- Order Assignment
- Delivery Tracking
- Notifications

Status:

Planned

---

# Features

- Microservices Architecture
- JWT Authentication
- Layered Architecture
- Repository Pattern
- Dependency Injection
- Alembic Database Migrations
- Dockerized Services
- API Gateway
- PostgreSQL
- Redis Caching *(Upcoming)*
- Kafka Event Streaming *(Upcoming)*

---

# Running the Project

Clone the repository

```bash
git clone https://github.com/<username>/food-delivery-platform.git

cd food-delivery-platform
```

Start the services

```bash
docker compose up --build
```

---

# Roadmap

- [x] Identity Service
- [x] Catalog Service
- [x] Order Service
- [x] Delivery Service
- [x] API Gateway
- [x] Redis Integration
- [x] Kafka Integration
- [ ] Background Jobs
- [x] Monitoring
- [ ] CI/CD Pipeline
- [ ] Kubernetes Deployment

---

# Learning Objectives

This project demonstrates practical implementation of:

- Microservices
- REST APIs
- Authentication & Authorization
- Docker
- Database Migrations
- Clean Architecture
- Dependency Injection
- Repository Pattern
- Event-Driven Architecture
- Distributed Systems

---