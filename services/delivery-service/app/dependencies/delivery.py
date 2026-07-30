from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.delivery_partner_repository import DeliveryPartnerRepository
from app.repositories.outbox_repository import OutboxRepository

from app.services.delivery_service import DeliveryService
from app.services.assignment_service import AssignmentService
from app.services.outbox_service import OutboxService


async def get_delivery_service(
    db: AsyncSession = Depends(get_db),
) -> DeliveryService:

    delivery_repository = DeliveryRepository(db)

    delivery_partner_repository = DeliveryPartnerRepository(db)

    outbox_repository = OutboxRepository(db)

    outbox_service = OutboxService(
        outbox_repository=outbox_repository,
    )

    assignment_service = AssignmentService(
        delivery_repository=delivery_repository,
        delivery_partner_repository=delivery_partner_repository,
        outbox_service=outbox_service,
    )

    return DeliveryService(
        delivery_repository=delivery_repository,
        outbox_service=outbox_service,
        assignment_service=assignment_service,
    )
    
    
# Now every API call has:
# DeliveryService
#         |
#         +-- DeliveryRepository
#         |
#         +-- OutboxService
#                 |
#                 +-- OutboxRepository