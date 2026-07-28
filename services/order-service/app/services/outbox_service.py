from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.order import Order
from app.models.outbox_event import OutboxEvent
from app.models.outbox_event_type import OutboxEventType
from app.repositories.outbox_repository import OutboxRepository


class OutboxService:

    def __init__(self, outbox_repository: OutboxRepository):
        self.outbox_repository = outbox_repository
        
    
    # def _build_order_data(self, order: Order) -> dict:
    #     return {
    #         "order_id": str(order.id),
    #         "customer_id": str(order.customer_id),
    #         "restaurant_id": str(order.restaurant_id),
    #         "status": order.status.value,
    #         "total_amount": float(order.total_amount),
    #     }

    async def _create_event(
        self,
        *,
        event_type: OutboxEventType,
        aggregate_type: str,
        aggregate_id: UUID,
        data: dict,
    ) -> OutboxEvent:

        payload = {
            "event_id": str(uuid4()),
            "event_type": event_type.value,
            "aggregate_type": aggregate_type,
            "aggregate_id": str(aggregate_id),
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "version": 1,
            "data": data,
        }

        event = OutboxEvent(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type.value,
            payload=payload,
        )

        return await self.outbox_repository.create(event)

    async def create_order_created(
        self,
        order: Order,
    ) -> OutboxEvent:

        return await self._create_event(
            event_type=OutboxEventType.ORDER_CREATED,
            aggregate_type="Order",
            aggregate_id=order.id,
            data={
                "order_id": str(order.id),
                "customer_id": str(order.customer_id),
                "restaurant_id": str(order.restaurant_id),
                "status": order.status.value,
                "total_amount": float(order.total_amount),
            },
        )

    async def create_order_status_updated(
        self,
        order: Order,
    ) -> OutboxEvent:

        return await self._create_event(
            event_type=OutboxEventType.ORDER_STATUS_UPDATED,
            aggregate_type="Order",
            aggregate_id=order.id,
            data={
                "order_id": str(order.id),
                "customer_id": str(order.customer_id),
                "restaurant_id": str(order.restaurant_id),
                "status": order.status.value,
            },
        )

    async def create_order_cancelled(
        self,
        order: Order,
    ) -> OutboxEvent:

        return await self._create_event(
            event_type=OutboxEventType.ORDER_CANCELLED,
            aggregate_type="Order",
            aggregate_id=order.id,
            data={
                "order_id": str(order.id),
                "customer_id": str(order.customer_id),
                "restaurant_id": str(order.restaurant_id),
                "status": order.status.value,
            },
        )