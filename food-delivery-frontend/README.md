# Food Delivery Platform

A production-oriented food delivery platform built as a microservices-based system using FastAPI, PostgreSQL, Kafka, Docker, React, and TypeScript.

The project demonstrates backend engineering practices including service separation, REST APIs, authentication, RBAC, asynchronous event-driven communication, the transactional outbox pattern, Saga-style distributed workflows, idempotency, retries, dead-letter queues, correlation/request IDs, health/readiness endpoints, and role-based frontend navigation.

---

## 1. Architecture

```text
                         ┌─────────────────────┐
                         │      React App       │
                         │  React + TypeScript  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     API Gateway     │
                         │       FastAPI       │
                         └──────┬──────┬───────┘
                                │      │
                  ┌─────────────┘      └──────────────┐
                  ▼                                   ▼
        ┌──────────────────┐                ┌──────────────────┐
        │ Identity Service │                │ Catalog Service  │
        │                  │                │                  │
        │ Auth / Users     │                │ Restaurants      │
        │ JWT / RBAC       │                │ Categories       │
        └────────┬─────────┘                │ Menu Items       │
                 │                          └────────┬─────────┘
                 │                                   │
                 │                    HTTP/gRPC      │
                 │                                   │
                 │                                   ▼
                 │                          ┌──────────────────┐
                 │                          │   Order Service  │
                 │                          │                  │
                 │                          │ Orders           │
                 │                          │ Order Items      │
                 │                          │ Idempotency      │
                 │                          │ Outbox           │
                 │                          └────────┬─────────┘
                 │                                   │
                 │                                   │ Kafka
                 │                                   ▼
                 │                          ┌──────────────────┐
                 │                          │ Delivery Service │
                 │                          │                  │
                 │                          │ Deliveries       │
                 │                          │ Assignment       │
                 │                          │ Delivery Status  │
                 │                          │ Outbox           │
                 │                          └────────┬─────────┘
                 │                                   │
                 │                                   │ Kafka
                 │                                   ▼
                 │                          ┌──────────────────┐
                 │                          │ Notification     │
                 │                          │ Service          │
                 │                          │                  │
                 │                          │ Notifications   │
                 │                          │ Read / Unread    │
                 │                          └──────────────────┘
                 │
                 ▼
        ┌──────────────────┐
        │    PostgreSQL    │
        │     Supabase     │
        └──────────────────┘

                         ┌─────────────────────┐
                         │        Kafka        │
                         │       Aiven         │
                         └─────────────────────┘
```

---

# 2. Services

## Identity Service

Responsible for authentication and users.

Responsibilities:

- User registration
- Login
- JWT access tokens
- Refresh tokens
- Current-user lookup
- Role-based authorization

Supported roles:

```text
CUSTOMER
RESTAURANT_OWNER
DELIVERY_PARTNER
ADMIN
```

---

## Catalog Service

Responsible for restaurant and menu management.

Entities:

```text
Restaurant
Category
MenuItem
```

Capabilities:

- Create restaurant
- Get restaurants
- Get restaurant
- Update restaurant
- Delete restaurant
- Create/update categories
- Create/update menu items
- Internal restaurant owner lookup
- Internal menu-item lookup

The Order Service communicates with Catalog Service over HTTP.

---

## Order Service

Responsible for customer orders.

Entities:

```text
Order
OrderItem
IdempotencyKey
OutboxEvent
```

Capabilities:

- Create order
- Get customer orders
- Get restaurant orders
- Get order
- Update order status
- Restaurant-owner authorization
- Idempotent order creation
- Transactional outbox
- Kafka event publishing
- Order state-transition validation

Order lifecycle:

```text
PENDING
   ↓
CONFIRMED
   ↓
PREPARING
   ↓
READY
   ↓
DELIVERED
```

Cancellation is handled as a separate terminal state where allowed.

---

## Delivery Service

Responsible for delivery lifecycle and delivery partners.

Entities:

```text
Delivery
DeliveryPartner
OutboxEvent
```

Capabilities:

- Get my deliveries
- Get delivery by order
- Get all deliveries for admin
- Assign delivery partner
- Update delivery status
- Cancel delivery
- Automatic delivery creation after an order reaches READY
- Delivery event publishing
- Kafka consumption
- Retry handling
- Dead Letter Queue handling

Delivery lifecycle:

```text
PENDING
   ↓
ASSIGNED
   ↓
PICKED_UP
   ↓
DELIVERED
```

Cancellation:

```text
PENDING / ASSIGNED / PICKED_UP
          ↓
      CANCELLED
```

---

## Notification Service

Responsible for user-facing notifications generated from domain events.

Capabilities:

- Get authenticated user's notifications
- Mark one notification as read
- Mark all notifications as read
- Consume business events from Kafka
- Create notifications without tightly coupling core business services to notification logic

Notification APIs:

```http
GET   /api/notifications/me
PATCH /api/notifications/{notification_id}/read
PATCH /api/notifications/read-all
```

Typical notification events include:

```text
Order confirmed
Order preparing
Order ready
Delivery assigned
Delivery picked up
Delivery delivered
Order cancelled
```

The notification service is intentionally event-driven.

```text
Order / Delivery Service
          │
          ▼
       Kafka
          │
          ▼
Notification Service
          │
          ▼
Create Notification
          │
          ▼
       Customer
```

---

## API Gateway

The gateway is the frontend's entry point.

Responsibilities:

- Route requests to backend services
- Forward authentication headers
- Centralize request/correlation ID propagation
- Provide a stable frontend API surface
- Hide internal service URLs

Example:

```text
/api/auth/*           → Identity Service
/api/restaurants/*    → Catalog Service
/api/orders/*         → Order Service
/api/deliveries/*     → Delivery Service
/api/notifications/* → Notification Service
```

---

# 3. Frontend

The frontend is built with:

- React
- TypeScript
- React Router
- Mantine UI
- TanStack React Query
- Zustand
- Tabler Icons

Frontend structure:

```text
frontend/
├── src/
│   ├── app/
│   │   ├── layouts/
│   │   └── router/
│   │
│   ├── modules/
│   │   ├── auth/
│   │   ├── restaurants/
│   │   ├── cart/
│   │   ├── orders/
│   │   ├── delivery/
│   │   ├── notifications/
│   │   └── dashboard/
│   │
│   └── shared/
│       ├── api/
│       ├── components/
│       ├── store/
│       └── constants/
```

Authentication state is persisted using Zustand.

The application uses role-based navigation:

```text
CUSTOMER
  → Restaurants
  → Cart
  → Orders
  → Notifications

RESTAURANT_OWNER
  → Restaurants
  → Restaurant Orders
  → Notifications

DELIVERY_PARTNER
  → Delivery Dashboard
  → Notifications

ADMIN
  → All Deliveries
  → Notifications
```

The application header contains:

```text
Cart
Notifications
Profile
Logout
```

The notification icon can display an unread counter.

---

# 4. End-to-End Business Flow

The primary order-to-delivery workflow is:

```text
Customer
   │
   ▼
Login
   │
   ▼
Browse Restaurants
   │
   ▼
Browse Menu
   │
   ▼
Add Items to Cart
   │
   ▼
Create Order
   │
   ▼
Order Service
   │
   ├── Save Order
   ├── Save Order Items
   └── Save Outbox Event
           │
           ▼
        Kafka
           │
           ▼
   Restaurant Owner
           │
           ▼
      CONFIRMED
           │
           ▼
      PREPARING
           │
           ▼
        READY
           │
           ▼
        Kafka
           │
           ▼
   Delivery Service
           │
           ▼
    Create Delivery
           │
           ▼
      ASSIGNED
           │
           ▼
      PICKED_UP
           │
           ▼
      DELIVERED
           │
           ▼
        Kafka
           │
           ▼
     Order Service
           │
           ▼
   Order = DELIVERED
```

Notifications are generated from the relevant domain events:

```text
Order / Delivery Event
        │
        ▼
      Kafka
        │
        ▼
Notification Service
        │
        ▼
Notification Created
        │
        ▼
Customer / Restaurant Owner / Delivery Partner
```

---

# 5. Event-Driven Architecture

Kafka is used for asynchronous communication between services.

Important events include:

```text
OrderCreated
OrderStatusUpdated
DeliveryCreated
DeliveryStatusUpdated
```

The exact event set can evolve as additional business workflows are introduced.

Example `OrderStatusUpdated` event:

```json
{
  "event_id": "001083d4-be50-4e4b-8d91-4218657df2c3",
  "event_type": "OrderStatusUpdated",
  "aggregate_type": "Order",
  "aggregate_id": "13535c33-0843-43f1-994c-087bf676ce9e",
  "occurred_at": "2026-08-06T06:34:06.840608+00:00",
  "version": 1,
  "data": {
    "status": "READY",
    "order_id": "13535c33-0843-43f1-994c-087bf676ce9e",
    "customer_id": "fb773945-9a0e-4b3a-adc3-801ab3a97a69",
    "restaurant_id": "47eefb93-4340-40a0-83c6-bea1bfcb68c5"
  }
}
```

---

# 6. Transactional Outbox Pattern

Services do not directly publish important business events as part of the database transaction.

Instead:

```text
Business Transaction
       │
       ├── Update business data
       │
       └── Insert Outbox Event
                │
                ▼
             COMMIT
                │
                ▼
         Outbox Publisher
                │
                ▼
              Kafka
```

This prevents the classic failure:

```text
Database transaction succeeds
        +
Kafka publish fails
        =
Database and event state diverge
```

The outbox pattern ensures the event is stored transactionally with the business change.

The same pattern is used where a service needs reliable event publication.

---

# 7. Saga Pattern

The order-to-delivery workflow spans multiple independent services and databases. A distributed transaction across all services is intentionally avoided.

Instead, the platform uses an event-driven Saga-style workflow.

## What is the Saga Pattern?

A Saga breaks a distributed business transaction into a sequence of local transactions.

Each service:

1. Performs its own local transaction.
2. Commits its database changes.
3. Publishes an event.
4. The next service reacts to that event.
5. If a later step fails, the workflow can use a compensating action where the business rules support one.

Conceptually:

```text
Local Transaction A
        │
        ▼
     Event A
        │
        ▼
Local Transaction B
        │
        ▼
     Event B
        │
        ▼
Local Transaction C
```

---

## Current Saga Flow

The current order-to-delivery workflow is primarily **choreography-based**.

There is no central Saga orchestrator controlling every step.

Instead, services react to domain events:

```text
Order Service
     │
     │ OrderStatusUpdated
     ▼
   Kafka
     │
     ▼
Delivery Service
     │
     │ DeliveryCreated / DeliveryStatusUpdated
     ▼
   Kafka
     │
     ▼
Order Service
```

For the main business flow:

```text
Order = READY
      │
      ▼
Order Service commits state
      │
      ▼
Outbox Event
      │
      ▼
Kafka
      │
      ▼
Delivery Service
      │
      ▼
Create Delivery
      │
      ▼
Assign Partner
      │
      ▼
Pick Up
      │
      ▼
Deliver
      │
      ▼
Delivery Event
      │
      ▼
Kafka
      │
      ▼
Order Service
      │
      ▼
Order = DELIVERED
```

This is a Saga because the complete business process is distributed across multiple local transactions.

---

## Saga Failure Handling

A Saga must not rely on database rollback across services.

For example:

```text
Order Service
    │
    ▼
READY
    │
    ▼
Kafka
    │
    ▼
Delivery Service
    │
    X
Delivery creation fails
```

The Order Service cannot simply roll back its database transaction because the original transaction has already committed.

Instead, the system needs one of:

```text
Retry
   OR
Dead Letter Queue
   OR
Compensating Event
   OR
Manual Recovery
```

The current implementation already provides retry and DLQ mechanisms for Kafka consumers.

Future compensation examples could include:

```text
Delivery creation permanently fails
        ↓
Publish DeliveryCreationFailed
        ↓
Order Service consumes event
        ↓
Order = DELIVERY_FAILED
```

Another possible compensation:

```text
Delivery cancelled
        ↓
DeliveryCancelled
        ↓
Order Service
        ↓
Order = DELIVERY_FAILED / CANCELLED
```

The exact compensating states should be defined according to business requirements before implementation.

---

## Choreography vs Orchestration

### Choreography

Each service listens to events and decides what to do.

```text
Order Service
     │
     ▼
   Kafka
     │
     ▼
Delivery Service
     │
     ▼
   Kafka
     │
     ▼
Order Service
```

Advantages:

- Loose coupling
- No central coordinator
- Services remain autonomous
- Natural fit for Kafka

Disadvantages:

- Workflow can become difficult to understand
- Business flow is distributed across consumers
- Debugging complex workflows becomes harder
- Event dependencies can become difficult to manage

### Orchestration

A dedicated Saga Orchestrator controls the workflow.

```text
             ┌──────────────────┐
             │ Saga Orchestrator │
             └────────┬─────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Order       Delivery   Notification
       Service      Service      Service
```

An orchestrator can be useful when workflows become significantly more complex.

For the current platform, choreography is sufficient because the order-to-delivery workflow is relatively small.

---

# 8. Kafka Consumer Reliability

Consumers use:

- Consumer groups
- Retry attempts
- Exponential backoff
- Dead Letter Queue
- Structured logging

Current retry strategy:

```text
Attempt 1
   ↓
wait 2 seconds
   ↓
Attempt 2
   ↓
wait 4 seconds
   ↓
Attempt 3
   ↓
DLQ
```

Failed events can be published to:

```text
orders-dlq
```

The DLQ allows failed events to be inspected and recovered without blocking the main consumer indefinitely.

---

# 9. Notifications

Notifications are generated from domain events instead of tightly coupling business services directly to the Notification Service.

Example:

```text
Customer places order
        │
        ▼
Order Service
        │
        ▼
OrderCreated
        │
        ▼
     Outbox
        │
        ▼
      Kafka
        │
        ▼
Notification Service
        │
        ▼
Create Notification
        │
        ▼
Customer
```

For order status updates:

```text
Restaurant
    │
    ▼
Order Status = READY
    │
    ▼
Order Service
    │
    ▼
OrderStatusUpdated
    │
    ▼
Kafka
    │
    ▼
Notification Service
    │
    ▼
Notification
    │
    ▼
Customer
```

For delivery events:

```text
Delivery Service
      │
      ▼
DeliveryStatusUpdated
      │
      ▼
Kafka
      │
      ▼
Notification Service
      │
      ▼
Customer Notification
```

---

## Notification Lifecycle

```text
Notification Created
        │
        ▼
      UNREAD
        │
        ├──────────────┐
        │              │
        ▼              ▼
Mark Read       Mark All Read
        │              │
        └──────┬───────┘
               ▼
             READ
```

A notification must belong to the authenticated user performing the read operation.

---

## Notification APIs

### Get My Notifications

```http
GET /api/notifications/me
```

Returns notifications belonging to the authenticated user.

### Mark Notification Read

```http
PATCH /api/notifications/{notification_id}/read
```

Marks one notification as read.

### Mark All Notifications Read

```http
PATCH /api/notifications/read-all
```

Marks all notifications belonging to the authenticated user as read.

---

# 10. Request IDs and Correlation IDs

HTTP requests carry request IDs/correlation IDs through the gateway and downstream services.

Example:

```text
Client
  │
  │ X-Request-ID
  ▼
Gateway
  │
  │ X-Request-ID
  ▼
Order Service
  │
  │ correlation metadata
  ▼
Kafka
  │
  ▼
Delivery Service
```

This makes it possible to trace one business operation across:

```text
Frontend
→ Gateway
→ Order Service
→ Kafka
→ Delivery Service
→ Notification Service
```

Structured logs include the request/correlation identifier where applicable.

For Kafka, event metadata should carry correlation information so asynchronous processing can be connected back to the original request.

---

# 11. Database

PostgreSQL is used as the primary database.

Supabase PostgreSQL is currently used for hosted environments.

Logical schemas include:

```text
orders
delivery
```

Typical Order Service tables:

```text
orders.orders
orders.order_items
orders.idempotency_keys
orders.outbox_events
```

Typical Delivery Service tables:

```text
delivery.deliveries
delivery.delivery_partners
delivery.outbox_events
```

Notification persistence contains user notification records and their read state.

Each service owns its business logic and persistence layer even when the development environment uses a shared PostgreSQL instance.

For a true production microservice deployment, separate database ownership per service is preferable.

---

# 12. Authentication

JWT authentication is used.

Typical JWT claims:

```json
{
  "sub": "user-id",
  "role": "CUSTOMER",
  "type": "access",
  "exp": 1234567890
}
```

Frontend authentication flow:

```text
Login
  ↓
Receive access + refresh token
  ↓
Store tokens in Zustand
  ↓
Fetch current user
  ↓
Store user
  ↓
Role-based redirect
  ↓
Protected application
```

Role-based redirects:

```text
CUSTOMER
    → /restaurants

RESTAURANT_OWNER
    → /owner/restaurants

ADMIN
    → /admin/deliveries

DELIVERY_PARTNER
    → /delivery
```

The frontend persists authentication state using Zustand.

Unauthenticated users are redirected to `/login`.

---

# 13. API Examples

## Authentication

```http
POST /api/auth/signup
POST /api/auth/login
GET  /api/auth/me
```

## Restaurants

```http
POST   /api/restaurants
GET    /api/restaurants
GET    /api/restaurants/{restaurant_id}
PUT    /api/restaurants/{restaurant_id}
DELETE /api/restaurants/{restaurant_id}
```

## Orders

```http
POST  /api/orders
GET   /api/orders/me
GET   /api/orders/restaurant/{restaurant_id}
GET   /api/orders/{order_id}
PATCH /api/orders/{order_id}/status
```

## Deliveries

```http
GET   /api/deliveries/me
GET   /api/deliveries
GET   /api/deliveries/{order_id}

PATCH /api/deliveries/{order_id}/assign
PATCH /api/deliveries/{order_id}/status
PATCH /api/deliveries/{order_id}/cancel
```

## Notifications

```http
GET   /api/notifications/me
PATCH /api/notifications/{notification_id}/read
PATCH /api/notifications/read-all
```

---

# 14. Delivery Status Updates

Delivery status transitions are validated by the Delivery Service.

Normal lifecycle:

```text
PENDING
   ↓
ASSIGNED
   ↓
PICKED_UP
   ↓
DELIVERED
```

Invalid transitions are rejected.

For example:

```text
PICKED_UP → PICKED_UP
```

is invalid because the delivery is already in the `PICKED_UP` state.

The service validates the current state before applying the requested transition.

---

# 15. Order Authorization

Restaurant order management is protected by restaurant ownership.

The Order Service:

1. Receives the authenticated user.
2. Identifies the restaurant.
3. Calls Catalog Service for restaurant ownership.
4. Compares restaurant owner ID with current user ID.
5. Rejects unauthorized access with `403`.

Example:

```text
Restaurant Owner
       │
       ▼
GET /owner/restaurants/{restaurant_id}/orders
       │
       ▼
Order Service
       │
       ▼
Catalog Service
       │
       ▼
owner_id
       │
       ▼
Compare with current_user.user_id
       │
   ┌───┴────┐
   │        │
 MATCH    NO MATCH
   │        │
   ▼        ▼
 Allow     403
```

---

# 16. Idempotency

Order creation supports idempotency keys.

Purpose:

Prevent duplicate orders when the client retries the same request.

Example:

```http
POST /api/orders
Idempotency-Key: 4a8e...
```

If the same idempotency key is submitted again, the service can return the previously created result instead of creating another order.

Idempotency is especially important in distributed systems because clients, gateways, and network connections can retry requests.

---

# 17. Health and Readiness

Services expose health/readiness endpoints.

Typical endpoints:

```http
GET /health
GET /ready
```

Health checks determine whether the application process is alive.

Readiness checks can be used to determine whether dependencies required by the service are available.

---

# 18. Docker

Services are containerized using Docker.

Typical Dockerfile pattern:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

---

# 19. Local Development

## Backend

Create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run a service:

```bash
uvicorn app.main:app --reload --port 8000
```

---

## Frontend

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

---

# 20. Environment Variables

Each service should provide its own environment configuration.

Typical variables include:

```env
DATABASE_URL=
CATALOG_SERVICE_URL=
IDENTITY_SERVICE_URL=
DELIVERY_SERVICE_URL=
NOTIFICATION_SERVICE_URL=

KAFKA_BOOTSTRAP_SERVERS=
KAFKA_SECURITY_PROTOCOL=
KAFKA_SASL_MECHANISM=
KAFKA_USERNAME=
KAFKA_PASSWORD=
KAFKA_SSL_CA_LOCATION=
```

JWT configuration may include:

```env
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=
```

Never commit production credentials or secrets to Git.

---

# 21. Alembic

Database migrations are managed with Alembic.

Create migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback one migration:

```bash
alembic downgrade -1
```

Check current revision:

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

---

# 22. Testing

Backend tests use `pytest`.

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_order_idempotency.py
```

The project includes tests around areas such as:

- Authentication
- Order creation
- Idempotency
- Authorization
- Order status transitions
- Delivery status transitions
- Service behavior

Recommended future tests include:

- Kafka consumer integration tests
- Outbox publisher tests
- Saga failure/compensation tests
- Notification consumer tests
- API contract tests
- End-to-end order-to-delivery tests

---

# 23. Deployment

Current deployment architecture uses:

```text
Frontend
   ↓
Hosted frontend

API Gateway
   ↓
Render

Identity Service
   ↓
Render

Catalog Service
   ↓
Render

Order Service
   ↓
Render

Delivery Service
   ↓
Render

Notification Service
   ↓
Render

PostgreSQL
   ↓
Supabase

Kafka
   ↓
Aiven Kafka
```

Render environment variables must be configured independently for each service.

The Kafka CA certificate must also be available inside services that connect using SASL_SSL.

---

# 24. Production Concerns Already Addressed

The project intentionally includes several production-oriented patterns:

- Microservice separation
- REST APIs
- JWT authentication
- RBAC
- PostgreSQL
- SQLAlchemy 2.0
- Async database access
- Alembic migrations
- HTTP service-to-service communication
- Kafka
- Transactional Outbox
- Saga-style event-driven workflow
- Retry with exponential backoff
- Dead Letter Queue
- Idempotency
- Request IDs
- Correlation IDs
- Structured logging
- Health endpoints
- Readiness endpoints
- Docker
- Cloud deployment
- Role-based frontend routing
- Persistent frontend authentication state
- State-machine validation for order/delivery statuses
- Event-driven notifications

---

# 25. Current Business State

The implemented order-to-delivery workflow is:

```text
Customer places order
        │
        ▼
Order Service
        │
        ▼
Order = PENDING
        │
        ▼
Restaurant confirms
        │
        ▼
Order = CONFIRMED
        │
        ▼
Restaurant starts preparation
        │
        ▼
Order = PREPARING
        │
        ▼
Restaurant marks ready
        │
        ▼
Order = READY
        │
        ▼
OrderStatusUpdated event
        │
        ▼
Kafka
        │
        ▼
Delivery Service
        │
        ▼
Delivery created
        │
        ▼
Delivery assigned
        │
        ▼
Delivery partner picks up
        │
        ▼
Delivery = DELIVERED
        │
        ▼
Delivery event
        │
        ▼
Kafka
        │
        ▼
Order Service
        │
        ▼
Order = DELIVERED
```

Notifications run alongside this workflow:

```text
Domain Event
     │
     ▼
Kafka
     │
     ├───────────────► Delivery Service
     │
     └───────────────► Notification Service
                              │
                              ▼
                         User Notification
```

---

# 26. Important Design Decisions

## Catalog communication

Catalog communication was initially implemented using gRPC.

For cloud deployment, it was changed to HTTP because the deployment environment made HTTP service-to-service communication simpler.

Current architecture:

```text
Order Service
      │
      │ HTTP
      ▼
Catalog Service
```

---

## Event publishing

Business events use the transactional outbox pattern instead of relying on direct Kafka publishing inside business transactions.

```text
Database transaction
       +
Outbox event
       ↓
    Commit
       ↓
Outbox worker
       ↓
     Kafka
```

---

## Delivery creation

Delivery creation is event-driven.

The Delivery Service does not need the Order Service to synchronously call it when an order becomes READY.

Instead:

```text
Order READY
   ↓
Outbox
   ↓
Kafka
   ↓
Delivery Consumer
   ↓
Create Delivery
```

---

## Notifications

Notification generation is also event-driven.

Core business services should publish domain events rather than directly depending on the Notification Service.

```text
Order / Delivery
      │
      ▼
    Kafka
      │
      ▼
Notification Service
      │
      ▼
Notification
```

This prevents notification failures from directly blocking core order or delivery transactions.

---

## Saga

The current distributed order-to-delivery workflow follows a choreography-style Saga.

Each service owns its local transaction and reacts to events produced by other services.

```text
Order Service
      │
      ▼
    Kafka
      │
      ▼
Delivery Service
      │
      ▼
    Kafka
      │
      ▼
Order Service
```

Retries and DLQ handling are currently part of failure management.

Compensating transactions should be added for business scenarios that require explicit recovery states.

---

# 27. Future Improvements

Recommended next improvements include:

### Authentication

- Proper refresh-token rotation
- Token expiration handling in frontend
- Centralized authorization policies
- Password reset
- Email verification
- Dedicated delivery-partner authentication

### Notifications

- Notification dropdown in the frontend
- Unread notification badge
- Notification preferences
- Real-time notifications using WebSockets or Server-Sent Events
- Push/email notification providers
- Notification retry/DLQ handling
- Notification event deduplication

### Distributed Systems

- Stronger Kafka event versioning
- Event schema registry
- Consumer offset/error monitoring
- Distributed tracing
- OpenTelemetry
- Prometheus metrics
- Grafana dashboards
- Centralized log aggregation
- Kafka partitioning strategy
- Event replay strategy
- Consumer idempotency
- Better Saga compensation workflows

### Platform

- Redis caching
- Rate limiting
- API Gateway authorization policies
- Kubernetes deployment
- CI/CD pipeline
- Automated integration tests
- Contract testing between services
- Separate production databases per service
- Infrastructure as Code

### Business

- Automated delivery-partner assignment
- Restaurant availability
- Payment service
- Payment Saga
- Refund workflow
- Coupon/discount service
- Inventory management
- Order tracking
- Estimated delivery time
- Customer reviews and ratings

---

# 28. Project Goal

This project is designed as a practical demonstration of building a production-style backend system rather than a simple CRUD application.

The key engineering concepts demonstrated are:

```text
Microservices
+
REST
+
JWT / RBAC
+
PostgreSQL
+
Async SQLAlchemy
+
Kafka
+
Transactional Outbox
+
Saga Pattern
+
Event-driven Architecture
+
Idempotency
+
Retries
+
DLQ
+
Correlation IDs
+
Structured Logging
+
Docker
+
Cloud Deployment
+
Notifications
```

The goal is to demonstrate how these pieces work together to build a reliable distributed food delivery platform.

---

# 29. System Design Summary

At a high level, the platform demonstrates:

```text
                    ┌─────────────────┐
                    │     Client      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  API Gateway    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        │                    │                     │
        ▼                    ▼                     ▼
   Identity              Catalog                Order
   Service               Service               Service
                                                  │
                                                   │ Outbox
                                                   ▼
                                                 Kafka
                                                   │
                                                   ▼
                                              Delivery
                                               Service
                                                   │
                                                   │ Outbox
                                                   ▼
                                                 Kafka
                                                   │
                                                   ▼
                                            Notification
                                               Service
```

The system combines synchronous communication where request/response semantics are required and asynchronous messaging where services benefit from loose coupling and independent processing.

The transactional outbox provides reliable event publication, while the Saga-style workflow coordinates business processes that span multiple services without requiring distributed database transactions.
