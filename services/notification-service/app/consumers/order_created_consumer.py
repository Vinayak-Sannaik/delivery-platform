import json
import logging
import ssl

from uuid import UUID
from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.repositories.notification_repository import NotificationRepository
from app.repositories.processed_event_repository import ProcessedEventRepository
from app.schemas.order_created_event import OrderCreatedEvent
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class OrderCreatedConsumer:
    def __init__(self):
        kwargs = {
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group_id": "notification-service",
            "value_deserializer": lambda v: json.loads(
                v.decode("utf-8")
            ),
        }

        if settings.KAFKA_SECURITY_PROTOCOL == "SASL_SSL":
            ssl_context = ssl.create_default_context(
                cafile=settings.KAFKA_SSL_CA_LOCATION
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

                event = OrderCreatedEvent.model_validate(
                    message.value["data"]
                )

                async with AsyncSessionLocal() as db:

                    repository = NotificationRepository(db)
                    processed_event_repository = ProcessedEventRepository(db)
                    
                    event_id = UUID(message.value["event_id"])

                    processed = await processed_event_repository.exists(
                        event_id
                    )

                    if processed:
                        logger.info(
                            "Skipping duplicate event %s",
                            event_id,
                        )
                        continue

                    service = NotificationService(
                        notification_repository=repository,
                    )

                    await service.create_notification(
                        user_id=event.customer_id,
                        title="Order Placed",
                        message="Your order has been placed successfully.",
                        type="ORDER_CREATED",
                    )
                    
                    await processed_event_repository.create(
                        event_id=event_id,
                        event_type=message.value["event_type"],
                    )

                    await db.commit()

                    logger.info(
                        "Notification created for order %s",
                        event.order_id,
                    )

        finally:
            await self.consumer.stop()
            
    
    async def stop(self):
        await self.consumer.stop()