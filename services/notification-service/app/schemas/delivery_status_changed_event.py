from uuid import UUID

from pydantic import BaseModel


class DeliveryStatusChangedEvent(BaseModel):
    delivery_id: UUID
    order_id: UUID
    customer_id: UUID
    status: str