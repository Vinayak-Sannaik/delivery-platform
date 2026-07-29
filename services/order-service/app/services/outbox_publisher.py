from sqlalchemy.ext.asyncio import AsyncSession

from app.kafka.producer import KafkaProducer
from app.kafka.topics import ORDERS_TOPIC
from app.repositories.outbox_repository import OutboxRepository


class OutboxPublisher:
    def __init__(
        self,
        db: AsyncSession,
        outbox_repository: OutboxRepository,
        kafka_producer: KafkaProducer,
    ) -> None:
        self.db = db
        self.outbox_repository = outbox_repository
        self.kafka_producer = kafka_producer

    async def publish_pending_events(
        self,
        limit: int = 100,
    ) -> None:
        events = await self.outbox_repository.get_pending(limit)

        if not events:
            return

        try:
            for event in events:
                await self.kafka_producer.publish(
                    topic=ORDERS_TOPIC,
                    key=str(event.aggregate_id),
                    value=event.payload,
                )

                await self.outbox_repository.mark_published(event)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise