from uuid import UUID

from pydantic import BaseModel


class OrderCreatedEvent(BaseModel):
    order_id: UUID
    customer_id: UUID
    restaurant_id: UUID
    status: str
    total_amount: float