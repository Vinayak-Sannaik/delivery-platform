from fastapi import FastAPI
from app.core.config import settings

from app.routers.auth import router as auth_router
from app.routers.catalog import router as catalog_router
from app.middleware.auth import AuthenticationMiddleware

app = FastAPI(
    title="Food Delivery API Gateway",
    version="1.0.0",
)

# print("url: ", settings.IDENTITY_SERVICE_URL)
app.add_middleware(AuthenticationMiddleware)

app.include_router(auth_router)
app.include_router(catalog_router)