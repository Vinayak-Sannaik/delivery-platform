from datetime import datetime, timezone
from uuid import uuid4, UUID

from pydantic import BaseModel


class DeliveryStatusChangedEvent(BaseModel):
    event_id: UUID
    event_type: str
    occurred_at: datetime
    delivery_id: UUID
    order_id: UUID
    status: str

    @classmethod
    def create(
        cls,
        delivery_id: UUID,
        order_id: UUID,
        status: str,
    ):
        return cls(
            event_id=uuid4(),
            event_type="DeliveryStatusChanged",
            occurred_at=datetime.now(timezone.utc),
            delivery_id=delivery_id,
            order_id=order_id,
            status=status,
        )