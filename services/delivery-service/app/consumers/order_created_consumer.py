import asyncio
import json
import logging
import ssl

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.core.database import AsyncSessionLocal

from app.kafka.dlq_producer import DLQProducer

from app.repositories.delivery_partner_repository import (
    DeliveryPartnerRepository,
)
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.outbox_repository import OutboxRepository

from app.schemas.order_created_event import OrderReadyEvent

from app.services.assignment_service import AssignmentService
from app.services.delivery_service import DeliveryService
from app.services.outbox_service import OutboxService
from app.services.redis_lock_service import RedisLockService

logger = logging.getLogger(__name__)


class OrderCreatedConsumer:

    def __init__(self):

        kwargs = {
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group_id": "delivery-service",
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

        self.dlq_producer = DLQProducer()

    async def start(self):

        await self.consumer.start()
        await self.dlq_producer.start()

        logger.info(
            "Delivery order consumer started"
        )

        try:

            async for message in self.consumer:

                try:

                    payload = message.value

                    logger.info(
                        "Kafka event received: %s",
                        payload,
                    )

                    # --------------------------------
                    # 1. Read event type
                    # --------------------------------

                    event_type = payload.get(
                        "event_type"
                    )

                    logger.info(
                        "Event type: %s",
                        event_type,
                    )

                    # --------------------------------
                    # 2. Ignore events we don't handle
                    # --------------------------------

                    if event_type != "OrderStatusUpdated":

                        logger.info(
                            "Ignoring event type: %s",
                            event_type,
                        )

                        continue

                    # --------------------------------
                    # 3. Validate event data
                    # --------------------------------

                    event = OrderReadyEvent.model_validate(
                        payload["data"]
                    )

                    logger.info(
                        "Order status event received: "
                        "order=%s status=%s",
                        event.order_id,
                        event.status,
                    )

                    # --------------------------------
                    # 4. Only READY creates delivery
                    # --------------------------------

                    if event.status != "READY":

                        logger.info(
                            "Ignoring order %s because "
                            "status is %s",
                            event.order_id,
                            event.status,
                        )

                        continue

                    # --------------------------------
                    # 5. Process with retry
                    # --------------------------------

                    max_retries = 3

                    for attempt in range(
                        1,
                        max_retries + 1,
                    ):

                        try:

                            async with AsyncSessionLocal() as db:

                                # ----------------------------
                                # Repositories
                                # ----------------------------

                                outbox_repository = (
                                    OutboxRepository(db)
                                )

                                delivery_repository = (
                                    DeliveryRepository(db)
                                )

                                delivery_partner_repository = (
                                    DeliveryPartnerRepository(db)
                                )
                                
                                redis_lock_service = RedisLockService()

                                # ----------------------------
                                # Services
                                # ----------------------------

                                outbox_service = (
                                    OutboxService(
                                        outbox_repository=
                                        outbox_repository,
                                    )
                                )

                                assignment_service = (
                                    AssignmentService(
                                        delivery_repository=
                                        delivery_repository,

                                        delivery_partner_repository=
                                        delivery_partner_repository,

                                        outbox_service=
                                        outbox_service,
                                        
                                        redis_lock_service=redis_lock_service,
                                    )
                                )

                                service = DeliveryService(
                                    delivery_repository=
                                    delivery_repository,

                                    outbox_service=
                                    outbox_service,

                                    assignment_service=
                                    assignment_service,

                                    delivery_partner_repository=
                                    delivery_partner_repository,
                                )

                                # ----------------------------
                                # Create delivery
                                # ----------------------------

                                await service.create_from_order(
                                    event
                                )

                                await db.commit()

                            logger.info(
                                "Delivery successfully created "
                                "for order %s",
                                event.order_id,
                            )

                            break

                        except Exception as exc:

                            logger.exception(
                                "Delivery processing failed "
                                "attempt %s/%s",
                                attempt,
                                max_retries,
                            )

                            if attempt == max_retries:

                                await self.dlq_producer.publish(
                                    "orders-dlq",
                                    {
                                        "original_topic": "orders",
                                        "retry_count": attempt,
                                        "error": str(exc),
                                        "event": payload,
                                    },
                                )

                                logger.error(
                                    "Event moved to DLQ "
                                    "after %s attempts",
                                    max_retries,
                                )

                            else:

                                await asyncio.sleep(
                                    2 ** attempt
                                )

                except Exception:

                    logger.exception(
                        "Unexpected error while processing "
                        "Kafka message"
                    )

        finally:

            await self.consumer.stop()
            await self.dlq_producer.stop()

            logger.info(
                "Delivery order consumer stopped"
            )