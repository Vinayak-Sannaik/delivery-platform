import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.logging import setup_logging

from app.consumers.order_created_consumer import OrderCreatedConsumer
from app.consumers.delivery_assigned_consumer import DeliveryAssignedConsumer
from app.consumers.delivery_status_changed_consumer import DeliveryStatusChangedConsumer
from app.routers.notifications import router as notification_router
from app.middleware.request_id import RequestIdMiddleware

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    order_created_consumer = OrderCreatedConsumer()
    delivery_assigned_consumer = DeliveryAssignedConsumer()
    delivery_status_changed_consumer = DeliveryStatusChangedConsumer()


    order_created_task = asyncio.create_task(
        order_created_consumer.start()
    )

    delivery_assigned_task = asyncio.create_task(
        delivery_assigned_consumer.start()
    )
    
    delivery_status_changed_task = asyncio.create_task(
        delivery_status_changed_consumer.start()
    )
    

    try:
        yield

    finally:
        order_created_task.cancel()
        delivery_assigned_task.cancel()
        delivery_status_changed_task.cancel()

        try:
            await order_created_consumer.stop()
        except asyncio.CancelledError:
            pass

        try:
            await order_created_task
        except asyncio.CancelledError:
            pass

        try:
            await delivery_assigned_task
        except asyncio.CancelledError:
            pass
        
        try:
            await delivery_status_changed_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Notification Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RequestIdMiddleware)

app.include_router(notification_router)


@app.get("/health")
async def health():
    return {"status": "healthy"}