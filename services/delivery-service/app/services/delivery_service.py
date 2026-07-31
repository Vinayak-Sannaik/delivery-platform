from app.models.delivery import Delivery
from app.models.delivery_status import DeliveryStatus
from app.repositories.delivery_repository import DeliveryRepository
from app.schemas.order_created_event import OrderCreatedEvent
from app.services.outbox_service import OutboxService
from app.services.assignment_service import AssignmentService
from app.repositories.delivery_partner_repository import DeliveryPartnerRepository
from datetime import datetime, timezone

from app.schemas.auth import CurrentUser
from app.models.user import RoleEnum

import logging

logger = logging.getLogger(__name__)


VALID_TRANSITIONS = {
    DeliveryStatus.PENDING: [
        DeliveryStatus.ASSIGNED,
        DeliveryStatus.CANCELLED,
    ],
    DeliveryStatus.ASSIGNED: [
        DeliveryStatus.PICKED_UP,
        DeliveryStatus.CANCELLED,
    ],
    DeliveryStatus.PICKED_UP: [
        DeliveryStatus.DELIVERED,
    ],
}


class DeliveryService:
    def __init__(
        self,
        delivery_repository: DeliveryRepository,
        outbox_service: OutboxService,
        assignment_service: AssignmentService,
        delivery_partner_repository: DeliveryPartnerRepository
        
    ):
        self.delivery_repository = delivery_repository
        self.outbox_service = outbox_service
        self.assignment_service = assignment_service
        self.delivery_partner_repository = delivery_partner_repository

    async def create_from_order(
        self,
        event: OrderCreatedEvent,
    ) -> Delivery:
        
        logger.info("Creating delivery for order %s", event.order_id)
        print("Creating delivery for order %s", event.order_id)
        
        existing = await self.delivery_repository.get_by_order_id(
            event.order_id,
        )

        if existing:
            return existing

        delivery = Delivery(
            order_id=event.order_id,
            customer_id=event.customer_id,
            restaurant_id=event.restaurant_id,
            status=DeliveryStatus.PENDING,
        )

        # return await self.delivery_repository.create(delivery)
        # await self.assignment_service.assign_delivery(
        #     delivery
        # )
        
        await self.delivery_repository.create(delivery)

        await self.assignment_service.assign_delivery(delivery)

        return delivery
    
    
    async def get_by_order_id(
        self,
        order_id,
        current_user,
    ):
        delivery = await self.delivery_repository.get_by_order_id(
            order_id
        )

        if not delivery:
            raise ValueError("Delivery not found")

        if current_user.role == RoleEnum.ADMIN:
            return delivery

        if current_user.role == RoleEnum.CUSTOMER:
            if delivery.customer_id != current_user.user_id:
                raise PermissionError(
                    "You cannot access this delivery"
                )

        elif current_user.role == RoleEnum.DELIVERY_PARTNER:
            if delivery.delivery_partner_id != current_user.user_id:
                raise PermissionError(
                    "You are not assigned to this delivery"
                )

        else:
            raise PermissionError(
                "Access denied"
            )

        return delivery
        
    async def update_status(
        self,
        order_id,
        status,
        current_user: CurrentUser,
    ):
        delivery = await self.delivery_repository.get_by_order_id(
            order_id
        )

        if not delivery:
            raise ValueError("Delivery not found")

        if current_user.role != RoleEnum.DELIVERY_PARTNER:
            raise PermissionError(
                "Only delivery partners can update delivery status"
            )

        if delivery.delivery_partner_id != current_user.user_id:
            raise PermissionError(
                "You are not assigned to this delivery"
            )
            
            
        if delivery.status == DeliveryStatus.DELIVERED:
            raise ValueError(
                "Delivered delivery cannot be updated"
            )

        if delivery.status == DeliveryStatus.CANCELLED:
            raise ValueError(
                "Cancelled delivery cannot be updated"
            )
        
            
        allowed_statuses = VALID_TRANSITIONS.get(
            delivery.status,
            [],
        )

        if status not in allowed_statuses:
            raise ValueError(
                f"Invalid transition: {delivery.status} -> {status}"
            )

        delivery.status = status
        
        if status in (
            DeliveryStatus.DELIVERED,
            DeliveryStatus.CANCELLED,
        ):
            await self.release_delivery_partner(delivery)
        
        
        await self.outbox_service.create_event(
            aggregate_type="Delivery",
            aggregate_id=delivery.id,
            event_type="DeliveryStatusChanged",
            payload={
                "delivery_id": str(delivery.id),
                "order_id": str(delivery.order_id),
                "status": status.value,
                "customer_id": str(delivery.customer_id),
            },
        )

        updated_delivery = await self.delivery_repository.update(
            delivery
        )

        await self.delivery_repository.db.commit()

        return updated_delivery
    
    
    
    async def assign_partner(
        self,
        order_id,
        delivery_partner_id,
        current_user,
    ):
        delivery = await self.delivery_repository.get_by_order_id(
            order_id
        )

        if not delivery:
            raise ValueError("Delivery not found")

        if current_user.role != RoleEnum.ADMIN:
            raise PermissionError(
                "Only admin can assign delivery partner"
            )

        if delivery.status in (
            DeliveryStatus.DELIVERED,
            DeliveryStatus.CANCELLED,
        ):
            raise ValueError(
                f"Cannot assign partner when delivery status is {delivery.status}"
            )

        delivery.delivery_partner_id = delivery_partner_id
        delivery.status = DeliveryStatus.ASSIGNED
        
        await self.outbox_service.create_event(
            aggregate_type="Delivery",
            aggregate_id=delivery.id,
            event_type="DeliveryAssigned",
            payload={
                "delivery_id": str(delivery.id),
                "order_id": str(delivery.order_id),
                "delivery_partner_id": str(
                    delivery_partner_id
                ),
                "customer_id": str(delivery.customer_id),
                "status": delivery.status.value,
            },
        )

        updated_delivery = await self.delivery_repository.update(
            delivery
        )

        await self.delivery_repository.db.commit()

        return updated_delivery
    
    
    async def get_my_deliveries(
        self,
        current_user,
        skip: int = 0,
        limit: int = 10,
    ):
        return await self.delivery_repository.get_by_partner_id(
            delivery_partner_id=current_user.user_id,
            skip=skip,
            limit=limit,
        )
        
        
        
    async def cancel_delivery(
        self,
        order_id,
        current_user,
    ):
        delivery = await self.delivery_repository.get_by_order_id(
            order_id
        )

        if not delivery:
            raise ValueError("Delivery not found")

        if current_user.role not in (
            RoleEnum.ADMIN,
            RoleEnum.CUSTOMER,
        ):
            raise PermissionError(
                "Only customer or admin can cancel delivery"
            )

        if current_user.role == RoleEnum.CUSTOMER:
            if delivery.customer_id != current_user.user_id:
                raise PermissionError(
                    "You cannot cancel this delivery"
                )

        if delivery.status in (
            DeliveryStatus.DELIVERED,
            DeliveryStatus.CANCELLED,
        ):
            raise ValueError(
                "Delivery cannot be cancelled"
            )

        delivery.status = DeliveryStatus.CANCELLED
        
        await self.outbox_service.create_event(
            aggregate_type="Delivery",
            aggregate_id=delivery.id,
            event_type="DeliveryCancelled",
            payload={
                "delivery_id": str(delivery.id),
                "order_id": str(delivery.order_id),
                "status": delivery.status.value,
            },
        )

        updated_delivery = await self.delivery_repository.update(
            delivery
        )

        await self.delivery_repository.db.commit()

        return updated_delivery
    
    
    async def release_delivery_partner(
        self,
        delivery: Delivery,
    ):
        if delivery.delivery_partner_id is None:
            return

        partner = await self.delivery_partner_repository.get_by_user_id(
            delivery.delivery_partner_id
        )

        if partner:
            partner.is_available = True
            partner.updated_at = datetime.now(timezone.utc)
            await self.delivery_partner_repository.update(partner)