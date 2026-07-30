from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.delivery_repository import DeliveryRepository
from app.services.delivery_service import DeliveryService

from app.repositories.outbox_repository import OutboxRepository
from app.services.outbox_service import OutboxService


async def get_delivery_service(
    db: AsyncSession = Depends(get_db),
) -> DeliveryService:
    delivery_repository = DeliveryRepository(db)
    
    outbox_repository = OutboxRepository(db)

    outbox_service = OutboxService(
        outbox_repository
    )

    return DeliveryService(
        delivery_repository=delivery_repository,
        outbox_service=outbox_service,
    )
    
    
# Now every API call has:
# DeliveryService
#         |
#         +-- DeliveryRepository
#         |
#         +-- OutboxService
#                 |
#                 +-- OutboxRepository