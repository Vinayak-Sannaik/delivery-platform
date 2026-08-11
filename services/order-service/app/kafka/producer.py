
import json

from aiokafka import AIOKafkaProducer
import ssl

from app.core.config import settings


class KafkaProducer:

    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    # async def start(self) -> None:
    #     self._producer = AIOKafkaProducer(
    #         bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    #     )
    #     await self._producer.start()
    
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

    async def publish(
        self,
        topic: str,
        key: str,
        value: dict,
    ) -> None:
        if self._producer is None:
            raise RuntimeError("Kafka producer is not started")

        await self._producer.send_and_wait(
            topic=topic,
            key=key.encode("utf-8"),
            value=json.dumps(value).encode("utf-8"),
        )