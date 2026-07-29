import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.catalog_http_client import CatalogHttpClient
from app.core.database import AsyncSessionLocal
from app.kafka.producer import KafkaProducer
from app.routers.orders import router as order_router
from app.workers.outbox_worker import OutboxWorker


@asynccontextmanager
async def lifespan(app: FastAPI):
    catalog_client = CatalogHttpClient()
    app.state.catalog_client = catalog_client

    kafka_producer = KafkaProducer()
    await kafka_producer.start()

    outbox_worker = OutboxWorker(
        session_factory=AsyncSessionLocal,
        kafka_producer=kafka_producer,
    )

    worker_task = asyncio.create_task(outbox_worker.start())

    try:
        yield
    finally:
        worker_task.cancel()

        try:
            await worker_task
        except asyncio.CancelledError:
            pass

        await kafka_producer.stop()
        await catalog_client.close()


app = FastAPI(
    title="Order Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(order_router)


@app.get("/health")
async def health():
    return {"status": "ok"}