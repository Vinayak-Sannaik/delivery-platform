import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumers.order_created_consumer import OrderCreatedConsumer
from app.routers.notifications import router as notification_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    order_created_consumer = OrderCreatedConsumer()

    consumer_task = asyncio.create_task(
        order_created_consumer.start()
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
    title="Notification Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(notification_router)


@app.get("/health")
async def health():
    return {"status": "ok"}