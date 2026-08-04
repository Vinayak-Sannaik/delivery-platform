import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.logging import setup_logging

from app.consumers.order_created_consumer import OrderCreatedConsumer
from app.kafka.producer import KafkaProducer
from app.workers.outbox_worker import OutboxWorker
from app.core.database import AsyncSessionLocal
from app.routers.deliveries import router as delivery_router
from app.routers.delivery_partners import router as delivery_partner_router
from app.middleware.request_id import RequestIdMiddleware

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer = OrderCreatedConsumer()

    kafka_producer = KafkaProducer()

    outbox_worker = OutboxWorker(
        session_factory=AsyncSessionLocal,
        kafka_producer=kafka_producer,
    )

    consumer_task = None
    worker_task = None

    try:
        # Start Kafka producer
        await kafka_producer.start()

        # Start order-created consumer
        consumer_task = asyncio.create_task(
            consumer.start()
        )

        # Start outbox worker
        worker_task = asyncio.create_task(
            outbox_worker.start()
        )

        yield

    finally:
        # Stop order consumer
        if consumer_task:
            consumer_task.cancel()

            try:
                await consumer_task
            except asyncio.CancelledError:
                pass

        # Stop outbox worker
        await outbox_worker.stop()

        if worker_task:
            worker_task.cancel()

            try:
                await worker_task
            except asyncio.CancelledError:
                pass

        # Stop Kafka producer
        await kafka_producer.stop()


app = FastAPI(
    title="Delivery Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RequestIdMiddleware)

app.include_router(delivery_router)
app.include_router(delivery_partner_router)


@app.get("/health")
async def health():
    return {"status": "healthy"}