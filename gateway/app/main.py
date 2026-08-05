from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

from app.routers.auth import router as auth_router
from app.routers.catalog import router as catalog_router
from app.routers.order  import router as order_router
from app.routers.health  import router as health_router
from app.routers.system_status import router as system_status
from app.routers.delivery import router as delivery_router

from app.middleware.auth import AuthenticationMiddleware
from app.middleware.request_id import RequestIdMiddleware
from fastapi.middleware.cors import CORSMiddleware


setup_logging()

app = FastAPI(
    title="Food Delivery API Gateway",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(AuthenticationMiddleware)

app.include_router(system_status)
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(order_router)
app.include_router(health_router)
app.include_router(delivery_router)