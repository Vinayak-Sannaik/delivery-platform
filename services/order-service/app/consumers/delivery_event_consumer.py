import json
import logging
import ssl

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService

logger = logging.getLogger(__name__)


class DeliveryEventConsumer:
    def __init__(self):
        kwargs = {
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group_id": "order-service-delivery-events",
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
            "delivery-events",
            **kwargs,
        )

    async def start(self):
        logger.info("Starting DeliveryEventConsumer...")

        await self.consumer.start()

        logger.info("DeliveryEventConsumer connected to Kafka")

        try:
            async for message in self.consumer:
                logger.info(
                    "Delivery event received: %s",
                    message.value,
                )

                print(
                    "Delivery event received:",
                    message.value,
                )

                event = message.value

                async with AsyncSessionLocal() as db:
                    repository = OrderRepository(db)

                    service = OrderService(
                        order_repository=repository,
                    )

                    await service.handle_delivery_event(
                        event
                    )

                    await db.commit()

                    logger.info(
                        "Processed delivery event for order: %s",
                        event.get("payload", {}).get("order_id"),
                    )

        except Exception:
            logger.exception(
                "Error while processing delivery events"
            )
            raise

        finally:
            await self.consumer.stop()
            logger.info("DeliveryEventConsumer stopped")