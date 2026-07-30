import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumers.order_created_consumer import OrderCreatedConsumer
from app.routers.deliveries import router as delivery_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer = OrderCreatedConsumer()
    
    consumer_task = asyncio.create_task(
        consumer.start()
    )

    try:
        yield
    finally:
        consumer_task.cancel()

        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
        
app = FastAPI(
    title="Delivery Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(delivery_router)

@app.get("/health")
async def health():
    return {"status": "ok"}