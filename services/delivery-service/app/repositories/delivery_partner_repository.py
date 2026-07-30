from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.delivery_partner import DeliveryPartner


class DeliveryPartnerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_first_available(self) -> DeliveryPartner | None:
        result = await self.db.execute(
            select(DeliveryPartner)
            .where(DeliveryPartner.is_available.is_(True))
            .limit(1)
        )

        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> DeliveryPartner | None:
        result = await self.db.execute(
            select(DeliveryPartner).where(
                DeliveryPartner.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        partner: DeliveryPartner,
    ):
        self.db.add(partner)
        await self.db.flush()

    async def update(
        self,
        partner: DeliveryPartner,
    ):
        await self.db.flush()