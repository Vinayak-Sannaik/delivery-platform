# API Gateway

The API Gateway is the single entry point for all client requests in the Food Delivery Platform. It routes incoming requests to the appropriate microservice, hiding internal service details from clients.

As the platform grows, the gateway will also handle cross-cutting concerns such as authentication, logging, rate limiting, and request tracing.

---

# Responsibilities

Current Responsibilities

- Route incoming requests to the appropriate microservice.
- Forward HTTP requests and responses.
- Handle CORS.

Future Responsibilities

- JWT Authentication & Authorization
- Rate Limiting
- Request Logging
- Request ID / Correlation ID
- API Versioning
- Load Balancing
- Circuit Breaker
- Service Discovery
- Response Caching

---

# Tech Stack

- Python 3.12
- FastAPI
- HTTPX
- Uvicorn
- Docker

---

# Architecture

```text
                     Client
                        │
                        ▼
                  API Gateway
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Identity Service   Catalog Service   Order Service
        │                                │
        └───────────────┬────────────────┘
                        ▼
               Delivery Service
```

---

# Request Flow

```text
Client
   │
POST /auth/login
   │
   ▼
API Gateway
   │
   ▼
Identity Service
   │
   ▼
JWT Token
   │
   ▼
API Gateway
   │
   ▼
Client
```

---

# Planned Routes

| Gateway Route | Target Service |
|---------------|----------------|
| `/auth/*` | Identity Service |
| `/catalog/*` | Catalog Service |
| `/orders/*` | Order Service |
| `/delivery/*` | Delivery Service |

---

# Project Structure

```text
gateway/
│
├── app/
│   ├── core/            # Configuration
│   ├── routers/         # Gateway routes
│   ├── services/        # Proxy logic
│   ├── utils/           # Shared utilities
│   └── main.py
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# Environment Variables

Create a `.env` file.

```env
IDENTITY_SERVICE_URL=http://identity-service:8000
CATALOG_SERVICE_URL=http://catalog-service:8000
ORDER_SERVICE_URL=http://order-service:8000
DELIVERY_SERVICE_URL=http://delivery-service:8000
```

For production, these values will point to the deployed service URLs.

---

# Running Locally

## Docker

```bash
docker compose up --build
```

Gateway

```
http://localhost:8080
```

Swagger

```
http://localhost:8080/docs
```

---

## Local Development

Create a virtual environment

```bash
python -m venv .venv
```

Activate

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload --port 8080
```

---

# Current Status

- ✅ FastAPI project
- ✅ Request routing
- 🚧 Proxy requests to services
- 🚧 Dockerized
- 🚧 Deployment

---

# Future Improvements

- JWT Verification
- Authentication Middleware
- Request Logging
- Rate Limiting
- Correlation ID
- Retry Mechanism
- Circuit Breaker
- Service Discovery
- Load Balancing
- Metrics & Monitoring

---

# Role in the Platform

```text
                Frontend
                    │
                    ▼
              API Gateway
        ┌──────────┼──────────┐
        ▼          ▼          ▼
 Identity     Catalog      Order
 Service      Service      Service
                    │
                    ▼
             Delivery Service
```

The API Gateway acts as the single public entry point to the platform. Clients never communicate directly with internal microservices, allowing services to evolve independently while exposing a consistent API.