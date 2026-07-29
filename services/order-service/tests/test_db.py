from unittest.mock import AsyncMock, patch
import pytest

from app.kafka.producer import KafkaProducer  # Adjust path to match your module


@pytest.mark.asyncio
async def test_kafka():
    # Mock AIOKafkaProducer so no real network call happens
    with patch("app.kafka.producer.AIOKafkaProducer") as MockProducer:
        mock_instance = AsyncMock()
        MockProducer.return_value = mock_instance

        producer = KafkaProducer()
        await producer.start()

        await producer.publish(
            topic="orders",
            key="123",
            value={"message": "hello"},
        )

        await producer.stop()

        # Assertions to ensure the methods were actually invoked
        mock_instance.start.assert_called_once()
        mock_instance.send_and_wait.assert_called_once()
        mock_instance.stop.assert_called_once()