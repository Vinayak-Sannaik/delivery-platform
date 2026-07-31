from uuid import UUID

from pydantic import BaseModel


class DeliveryAssignedEvent(BaseModel):
    delivery_id: UUID
    order_id: UUID
    customer_id: UUID
    delivery_partner_id: UUID
    status: str