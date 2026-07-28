from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.outbox_event import OutboxEvent
from app.models.outbox_event_status import OutboxEventStatus
from datetime import timezone, datetime


class OutboxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event: OutboxEvent) -> OutboxEvent:
        self.db.add(event)
        await self.db.flush()
        return event

    async def get_pending(self, limit: int = 100) -> list[OutboxEvent]:
        stmt = select(OutboxEvent).where(OutboxEvent.status == OutboxEventStatus.PENDING).order_by(
            OutboxEvent.created_at.asc()).limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def mark_published(self, event: OutboxEvent) -> None:
        event.status = OutboxEventStatus.PUBLISHED
        event.published_at = datetime.now(timezone.utc)
        await self.db.flush()
        return event
