from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.delivery_repository import DeliveryRepository
from app.services.delivery_service import DeliveryService


async def get_delivery_service(
    db: AsyncSession = Depends(get_db),
) -> DeliveryService:
    delivery_repository = DeliveryRepository(db)

    return DeliveryService(
        delivery_repository=delivery_repository,
    )