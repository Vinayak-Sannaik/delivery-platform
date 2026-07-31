import json
import ssl

from aiokafka import AIOKafkaConsumer
import asyncio

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.repositories.delivery_repository import DeliveryRepository
from app.schemas.order_created_event import OrderCreatedEvent
from app.services.delivery_service import DeliveryService

from app.repositories.outbox_repository import OutboxRepository
from app.services.outbox_service import OutboxService

from app.repositories.delivery_partner_repository import DeliveryPartnerRepository
from app.services.assignment_service import AssignmentService

from app.kafka.dlq_producer import DLQProducer

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
        
        self.dlq_producer = DLQProducer()

    async def start(self):
        await self.consumer.start()
        await self.dlq_producer.start()

        try:
            async for message in self.consumer:

                event = OrderCreatedEvent.model_validate(
                    message.value["data"]
                )

                max_retries = 3

                for attempt in range(1, max_retries + 1):
                    try:
                        logger.info(
                            "Kafka message received: %s",
                            message.value,
                        )

                        async with AsyncSessionLocal() as db:

                            outbox_repository = OutboxRepository(db)

                            outbox_service = OutboxService(
                                outbox_repository=outbox_repository,
                            )

                            delivery_repository = DeliveryRepository(db)

                            delivery_partner_repository = (
                                DeliveryPartnerRepository(db)
                            )

                            assignment_service = AssignmentService(
                                delivery_repository=delivery_repository,
                                delivery_partner_repository=delivery_partner_repository,
                                outbox_service=outbox_service,
                            )

                            service = DeliveryService(
                                delivery_repository=delivery_repository,
                                outbox_service=outbox_service,
                                assignment_service=assignment_service,
                            )

                            await service.create_from_order(event)

                            await db.commit()

                        logger.info(
                            "Delivery created for order: %s",
                            event.order_id,
                        )

                        # Success
                        break

                    except Exception as e:
                        logger.exception(
                            "Attempt %s/%s failed",
                            attempt,
                            max_retries,
                        )

                        if attempt == max_retries:

                            await self.dlq_producer.publish(
                                "orders-dlq",
                                {
                                    "original_topic": "orders",
                                    "retry_count": attempt,
                                    "error": str(e),
                                    "event": message.value,
                                },
                            )

                        else:
                            await asyncio.sleep(2 ** attempt)

        finally:
            await self.consumer.stop()
            await self.dlq_producer.stop()