# 🍔 Food Delivery Platform

A production-inspired microservices-based Food Delivery Platform built to learn and demonstrate backend engineering concepts such as distributed systems, API Gateway, authentication, asynchronous communication, caching, and containerized deployments.

The project is designed using industry-standard architecture while remaining simple enough to understand and extend.

---

# 🚀 Live Services

| Service | Status | Live |
|----------|--------|------|
| Identity Service | ✅ Live | https://delivery-platform-xo8w.onrender.com/docs |
| Catalog Service | 🚧 In Progress | - |
| Order Service | 📋 Planned | - |
| Delivery Service | 📋 Planned | - |

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
- [ ] Catalog Service
- [ ] Order Service
- [ ] Delivery Service
- [ ] API Gateway
- [ ] Redis Integration
- [ ] Kafka Integration
- [ ] Background Jobs
- [ ] Monitoring
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

# License

This project is created for learning purposes and backend engineering interview preparation.