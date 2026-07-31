import json
from datetime import datetime, timezone

from app.repositories.outbox_repository import OutboxRepository
from app.kafka.producer import KafkaProducer


class OutboxPublisher:

    def __init__(
        self,
        db,
        outbox_repository: OutboxRepository,
        kafka_producer: KafkaProducer,
    ):
        self.db = db
        self.outbox_repository = outbox_repository
        self.kafka_producer = kafka_producer


    async def publish_pending_events(self):

        events = await self.outbox_repository.get_pending_events()

        for event in events:

            await self.kafka_producer.publish(
                topic="delivery-events",
                event={
                    "event_id": str(event.id),
                    "event_type": event.event_type,
                    "aggregate_id": str(event.aggregate_id),
                    "aggregate_type": event.aggregate_type,
                    "payload": event.payload,
                    "created_at": event.created_at.isoformat(),
                },
            )

            await self.outbox_repository.mark_published(
                event
            )

        await self.db.commit()