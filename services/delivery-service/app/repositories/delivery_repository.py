from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.delivery import Delivery


class DeliveryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        delivery: Delivery,
    ) -> Delivery:
        self.db.add(delivery)
        await self.db.flush()
        await self.db.refresh(delivery)
        return delivery

    async def get_by_order_id(
        self,
        order_id: UUID,
    ) -> Delivery | None:
        result = await self.db.execute(
            select(Delivery).where(
                Delivery.order_id == order_id
            )
        )

        return result.scalar_one_or_none()
    
    async def update(
        self,
        delivery: Delivery,
    ) -> Delivery:
        await self.db.flush()
        await self.db.refresh(delivery)

        return delivery