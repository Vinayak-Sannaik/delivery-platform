
import json

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class KafkaProducer:

    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        )
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