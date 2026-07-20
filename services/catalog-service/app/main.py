from fastapi import FastAPI

from app.routers.restaurant import router as restaurant_router
from app.routers.category import router as category_router

app = FastAPI(
    title="Catalog Service",
    version="1.0.0",
)

app.include_router(restaurant_router)
app.include_router(category_router)


@app.get("/health")
def health():
    return {"status": "ok"}