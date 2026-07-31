from app.models.status_enum import OrderStatus
from app.repositories.order_repository import OrderRepository
from app.models.delivery_events import DeliveryEventType
from app.models.status_enum import OrderStatus

import logging
logger = logging.getLogger(__name__)

class OrderEventService:
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def handle_delivery_event(
        self,
        event: dict,
    ):
        logger.info(
            "handle_delivery_event:-",
        )
        
        event_type = event.get("event_type")

        payload = event.get("payload", {})

        order_id = payload.get("order_id")

        order = await self.order_repository.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if event_type == DeliveryEventType.DELIVERY_ASSIGNED:
            order.status = OrderStatus.READY

        elif event_type == DeliveryEventType.DELIVERY_CANCELLED:
            order.status = OrderStatus.CANCELLED

        elif event_type == DeliveryEventType.DELIVERY_STATUS_CHANGED:
            if payload.get("status") == OrderStatus.DELIVERED:
                order.status = OrderStatus.DELIVERED

        await self.order_repository.update(order)
        
        logger.info(
            "handle_delivery_event end:-",
        )

        return order