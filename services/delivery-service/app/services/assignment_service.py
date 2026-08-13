from fastapi import HTTPException

from app.models.delivery_status import DeliveryStatus
from app.repositories.delivery_partner_repository import (
    DeliveryPartnerRepository,
)
from app.repositories.delivery_repository import DeliveryRepository
from app.services.outbox_service import OutboxService
from app.services.redis_lock_service import RedisLockService


class AssignmentService:

    def __init__(
        self,
        delivery_repository: DeliveryRepository,
        delivery_partner_repository: DeliveryPartnerRepository,
        outbox_service: OutboxService,
        redis_lock_service: RedisLockService,
    ):
        self.delivery_repository = delivery_repository
        self.delivery_partner_repository = (
            delivery_partner_repository
        )
        self.outbox_service = outbox_service
        self.redis_lock_service = redis_lock_service

    async def assign_delivery(
        self,
        delivery,
    ) -> bool:

        # Only assign deliveries that are not already assigned.
        if delivery.status != DeliveryStatus.PENDING:
            return False

        lock_key = f"delivery:assignment:{delivery.id}"

        lock_token = self.redis_lock_service.acquire(
            key=lock_key,
            ttl=10,
        )

        if lock_token is None:
            raise HTTPException(
                status_code=409,
                detail="Delivery is currently being assigned.",
            )

        try:
            # Check again after acquiring the lock.
            #
            # Another worker/request may have changed the
            # delivery before we acquired the lock.
            if delivery.status != DeliveryStatus.PENDING:
                return False

            partner = (
                await self.delivery_partner_repository
                .get_first_available()
            )

            if not partner:
                return False

            delivery.delivery_partner_id = partner.user_id
            delivery.status = DeliveryStatus.ASSIGNED

            partner.is_available = False

            await self.delivery_repository.update(
                delivery
            )

            await self.delivery_partner_repository.update(
                partner
            )

            await self.outbox_service.create_event(
                aggregate_type="Delivery",
                aggregate_id=delivery.id,
                event_type="DeliveryAssigned",
                payload={
                    "delivery_id": str(delivery.id),
                    "order_id": str(delivery.order_id),
                    "delivery_partner_id": str(
                        partner.user_id
                    ),
                    "customer_id": str(
                        delivery.customer_id
                    ),
                    "status": delivery.status.value,
                },
            )

            return True

        finally:
            self.redis_lock_service.release(
                key=lock_key,
                token=lock_token,
            )