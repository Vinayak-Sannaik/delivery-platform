import asyncio
import logging


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.kafka.producer import KafkaProducer
from app.repositories.outbox_repository import OutboxRepository
from app.services.outbox_publisher import OutboxPublisher

logger = logging.getLogger(__name__)

class OutboxWorker:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        kafka_producer: KafkaProducer,
        interval: int = 20,
    ):
        self.session_factory = session_factory
        self.kafka_producer = kafka_producer
        self.interval = interval

        self.running = True

    async def start(self):
        while self.running:
            try:
                async with self.session_factory() as db:
                    repository = OutboxRepository(db)

                    publisher = OutboxPublisher(
                        db=db,
                        outbox_repository=repository,
                        kafka_producer=self.kafka_producer,
                    )

                    await publisher.publish_pending_events()

            except Exception as e:
                logger.error(
                    "Outbox worker error:",
                    e,
                )

            await asyncio.sleep(self.interval)

    async def stop(self):
        self.running = False