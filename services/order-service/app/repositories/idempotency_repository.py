from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.idempotency_key import IdempotencyKey


class IdempotencyRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db


    async def get_by_key(
        self,
        key: str,
    ) -> IdempotencyKey | None:

        result = await self.db.execute(
            select(IdempotencyKey)
            .where(
                IdempotencyKey.key == key
            )
        )

        return result.scalar_one_or_none()


    async def create(
        self,
        key: str,
        customer_id: UUID,
        order_id: UUID,
    ) -> IdempotencyKey:

        record = IdempotencyKey(
            key=key,
            customer_id=customer_id,
            order_id=order_id,
        )

        self.db.add(record)

        await self.db.flush()

        return record