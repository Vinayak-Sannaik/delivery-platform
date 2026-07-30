import json
import ssl

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.repositories.delivery_repository import DeliveryRepository
from app.schemas.order_created_event import OrderCreatedEvent
from app.services.delivery_service import DeliveryService

import logging

logger = logging.getLogger(__name__)


class OrderCreatedConsumer:
    def __init__(self):
        kwargs = {
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group_id": "delivery-service",
            "value_deserializer": lambda v: json.loads(v.decode("utf-8")),
        }
        if settings.KAFKA_SECURITY_PROTOCOL == "SASL_SSL":
            ssl_context = ssl.create_default_context(
                cafile="certs/aiven-ca.pem",
            )

            kwargs.update(
                {
                    "security_protocol": settings.KAFKA_SECURITY_PROTOCOL,
                    "sasl_mechanism": settings.KAFKA_SASL_MECHANISM,
                    "sasl_plain_username": settings.KAFKA_USERNAME,
                    "sasl_plain_password": settings.KAFKA_PASSWORD,
                    "ssl_context": ssl_context,
                }
            )

        self.consumer = AIOKafkaConsumer(
            "orders",
            **kwargs,
        )

    async def start(self):
        await self.consumer.start()

        try:
            async for message in self.consumer:
                logger.info(
                    "Kafka message received: %s",
                    message.value,
                )
                print( "Kafka message received: %s",
                    message.value,)
                event = OrderCreatedEvent.model_validate(
                    message.value["data"]
                )

                async with AsyncSessionLocal() as db:
                    service = DeliveryService(
                        delivery_repository=DeliveryRepository(db),
                    )

                    await service.create_from_order(event)
                    
                    logger.info(
                        "Delivery created for order: %s",
                        event.order_id,
                    )
                    print("Delivery created for order: %s",
                        event.order_id,)

                    await db.commit()

        finally:
            await self.consumer.stop()