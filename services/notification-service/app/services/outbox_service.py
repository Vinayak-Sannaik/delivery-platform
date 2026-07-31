from uuid import UUID

from app.models.outbox_event import OutboxEvent
from app.repositories.outbox_repository import OutboxRepository


class OutboxService:
    def __init__(
        self,
        outbox_repository: OutboxRepository,
    ):
        self.outbox_repository = outbox_repository

    async def create_event(
        self,
        aggregate_type: str,
        aggregate_id: UUID,
        event_type: str,
        payload: dict,
    ):
        event = OutboxEvent(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload,
            status="PENDING",
        )

        return await self.outbox_repository.create(event)