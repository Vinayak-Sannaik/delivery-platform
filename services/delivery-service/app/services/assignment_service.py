from app.models.delivery_status import DeliveryStatus
from app.repositories.delivery_partner_repository import (
    DeliveryPartnerRepository,
)
from app.repositories.delivery_repository import DeliveryRepository
from app.services.outbox_service import OutboxService


class AssignmentService:
    def __init__(
        self,
        delivery_repository: DeliveryRepository,
        delivery_partner_repository: DeliveryPartnerRepository,
        outbox_service: OutboxService,
    ):
        self.delivery_repository = delivery_repository
        self.delivery_partner_repository = delivery_partner_repository
        self.outbox_service = outbox_service

    async def assign_delivery(
        self,
        delivery,
    ):
        # print("1. Looking for available partner")

        partner = await self.delivery_partner_repository.get_first_available()

        # print("2. Partner:", partner)

        if not partner:
            print("3. No partner found")
            return False

        # print("4. Updating delivery")

        delivery.delivery_partner_id = partner.user_id
        delivery.status = DeliveryStatus.ASSIGNED

        # print("5. Updating partner")

        partner.is_available = False

        await self.delivery_repository.update(delivery)

        # print("6. Delivery updated")

        await self.delivery_partner_repository.update(partner)

        # print("7. Partner updated")

        await self.outbox_service.create_event(
            aggregate_type="Delivery",
            aggregate_id=delivery.id,
            event_type="DeliveryAssigned",
            payload={
                "delivery_id": str(delivery.id),
                "order_id": str(delivery.order_id),
                "delivery_partner_id": str(partner.user_id),
                "status": delivery.status.value,
            },
        )

        # print("8. Outbox event created")

        return True