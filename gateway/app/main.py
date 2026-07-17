from fastapi import FastAPI
from app.core.config import settings

from app.routers.auth import router as auth_router

app = FastAPI(
    title="Food Delivery API Gateway",
    version="1.0.0",
)

# print("url: ", settings.IDENTITY_SERVICE_URL)

app.include_router(auth_router)