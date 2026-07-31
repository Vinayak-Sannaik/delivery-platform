from fastapi import FastAPI
from app.core.logging import setup_logging

from app.api.router import router
from app.core.config import settings
from app.middleware.request_id import RequestIdMiddleware

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(RequestIdMiddleware)

app.include_router(router)