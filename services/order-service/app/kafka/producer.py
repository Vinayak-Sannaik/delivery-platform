import json
import ssl
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaProducer

from app.core.config import settings
from app.schemas.event import EventEnvelope


class KafkaProducer:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        kwargs = {
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
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

        self._producer = AIOKafkaProducer(**kwargs)

        await self._producer.start()

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def publish(
        self,
        topic: str,
        key: str | UUID,
        event: EventEnvelope,
    ) -> None:
        if self._producer is None:
            raise RuntimeError(
                "Kafka producer is not started"
            )

        event = EventEnvelope(
            event_type="OrderStatusUpdated",
            aggregate_id=order.id,
            aggregate_type="Order",
            correlation_id=correlation_id,
            causation_id=causation_id,
            data={
                "order_id": order.id,
                "status": order.status,
                "customer_id": order.customer_id,
                "restaurant_id": order.restaurant_id,
            },
        )

        await producer.publish(
            topic="orders",
            key=order.id,
            event=event,
        )