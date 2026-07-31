from uuid import UUID

from sqlalchemy import select

from app.models.outbox_event import OutboxEvent


class OutboxRepository:
    def __init__(self, db):
        self.db = db

    async def create(
        self,
        event: OutboxEvent,
    ):
        self.db.add(event)
        await self.db.flush()

        return event

    async def get_pending_events(
        self,
        limit: int = 100,
    ):
        result = await self.db.execute(
            select(OutboxEvent)
            .where(
                OutboxEvent.status == "PENDING"
            )
            .limit(limit)
        )

        return result.scalars().all()

    async def mark_published(
        self,
        event: OutboxEvent,
    ):
        event.status = "PUBLISHED"

        await self.db.flush()

        return event