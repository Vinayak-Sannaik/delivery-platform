import json
import ssl

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class KafkaProducer:

    def __init__(self):
        ssl_context = ssl.create_default_context(
            cafile=settings.KAFKA_SSL_CA_LOCATION
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            security_protocol=settings.KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism=settings.KAFKA_SASL_MECHANISM,
            sasl_plain_username=settings.KAFKA_USERNAME,
            sasl_plain_password=settings.KAFKA_PASSWORD,
            ssl_context=ssl_context,
            value_serializer=lambda value: json.dumps(value).encode(
                "utf-8"
            ),
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def publish(
        self,
        topic: str,
        event: dict,
    ):
        await self.producer.send_and_wait(
            topic,
            event,
        )