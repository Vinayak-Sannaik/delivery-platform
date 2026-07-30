from app.models.delivery import Delivery
from app.models.delivery_status import DeliveryStatus
from app.repositories.delivery_repository import DeliveryRepository
from app.schemas.order_created_event import OrderCreatedEvent


class DeliveryService:
    def __init__(
        self,
        delivery_repository: DeliveryRepository,
    ):
        self.delivery_repository = delivery_repository

    async def create_from_order(
        self,
        event: OrderCreatedEvent,
    ) -> Delivery:
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

        return await self.delivery_repository.create(delivery)
    
    async def get_by_order_id(
        self,
        order_id,
    ):
        return await self.delivery_repository.get_by_order_id(
            order_id
        )
        
    async def update_status(
        self,
        order_id,
        status,
    ):
        delivery = await self.delivery_repository.get_by_order_id(
            order_id
        )

        if not delivery:
            raise ValueError("Delivery not found")

        delivery.status = status

        updated_delivery = await self.delivery_repository.update(
            delivery
        )

        await self.delivery_repository.db.commit()

        return updated_delivery