from app.models.status_enum import OrderStatus
from app.repositories.order_repository import OrderRepository


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
        event_type = event.get("event_type")

        payload = event.get("payload", {})

        order_id = payload.get("order_id")

        order = await self.order_repository.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if event_type == "DeliveryAssigned":
            order.status = OrderStatus.READY

        elif event_type == "DeliveryCancelled":
            order.status = OrderStatus.CANCELLED

        elif event_type == "DeliveryStatusChanged":
            if payload.get("status") == "DELIVERED":
                order.status = OrderStatus.DELIVERED

        await self.order_repository.update(order)

        return order