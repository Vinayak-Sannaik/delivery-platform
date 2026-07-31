import json
import ssl

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class DLQProducer:
    def __init__(self):
        kwargs = {
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
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

        self.producer = AIOKafkaProducer(**kwargs)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def publish(
        self,
        topic: str,
        message: dict,
    ):
        await self.producer.send_and_wait(
            topic,
            message,
        )