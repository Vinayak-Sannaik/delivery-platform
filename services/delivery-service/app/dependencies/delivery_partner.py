from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.delivery_partner_repository import (
    DeliveryPartnerRepository,
)
from app.services.delivery_partner_service import (
    DeliveryPartnerService,
)


async def get_delivery_partner_service(
    db: AsyncSession = Depends(get_db),
) -> DeliveryPartnerService:

    repository = DeliveryPartnerRepository(db)

    return DeliveryPartnerService(
        delivery_partner_repository=repository,
    )