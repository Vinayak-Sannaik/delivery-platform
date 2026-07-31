from uuid import UUID

from sqlalchemy import select

from app.models.processed_event import ProcessedEvent


class ProcessedEventRepository:

    def __init__(self, db):
        self.db = db

    async def exists(
        self,
        event_id: UUID,
    ):
        result = await self.db.execute(
            select(ProcessedEvent)
            .where(
                ProcessedEvent.event_id == event_id
            )
        )

        return result.scalar_one_or_none() is not None


    async def create(
        self,
        event_id: UUID,
        event_type: str,
    ):
        event = ProcessedEvent(
            event_id=event_id,
            event_type=event_type,
        )

        self.db.add(event)

        await self.db.flush()

        return event