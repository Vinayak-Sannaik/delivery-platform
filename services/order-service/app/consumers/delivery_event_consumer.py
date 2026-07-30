import json

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService

import logging

logger = logging.getLogger(__name__)

class DeliveryEventConsumer:

    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            "delivery-events",
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id="order-service-delivery-events",
            value_deserializer=lambda v: json.loads(
                v.decode("utf-8")
            ),
        )

    async def start(self):
        await self.consumer.start()

        try:
            async for message in self.consumer:

                print(
                    "Delivery event received:",
                    message.value,
                )
                logger.info(
                    "Kafka message received at order service: %s",
                    message.value,
                )

                event = message.value

                async with AsyncSessionLocal() as db:

                    repository = OrderRepository(db)

                    service = OrderService(
                        order_repository=repository,
                    )
                    
                    logger.info(
                        "Delivery assigned created for order: %s",
                        event.order_id,
                    )

                    await service.handle_delivery_event(
                        event
                    )

                    await db.commit()

        finally:
            await self.consumer.stop()