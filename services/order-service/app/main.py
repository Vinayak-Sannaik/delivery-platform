from fastapi import FastAPI

from app.routers.orders import router as order_router

app = FastAPI(
    title="Order Service",
    version="1.0.0",
)

app.include_router(order_router)


@app.get("/health")
async def health():
    return {"status": "ok"}