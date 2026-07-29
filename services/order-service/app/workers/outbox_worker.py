import asyncio

from app.services.outbox_publisher import OutboxPublisher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.repositories.outbox_repository import OutboxRepository
from app.kafka.producer import KafkaProducer


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

    async def start(self) -> None:
        while True:
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
                print(e)

            await asyncio.sleep(self.interval)