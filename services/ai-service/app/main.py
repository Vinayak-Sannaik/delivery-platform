from fastapi import FastAPI

from app.core.config import settings
from app.routers.chat import router as chat_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "ai_enabled": settings.ai_enabled,
    }


app.include_router(
    chat_router,
    # prefix="/api/ai",
)