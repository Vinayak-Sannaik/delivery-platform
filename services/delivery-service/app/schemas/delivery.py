from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

from app.models.delivery_status import DeliveryStatus

class UpdateDeliveryStatusRequest(BaseModel):
    status: DeliveryStatus
    
class AssignDeliveryPartnerRequest(BaseModel):
    delivery_partner_id: UUID
    
class DeliveryResponse(BaseModel):
    id: UUID
    order_id: UUID
    customer_id: UUID
    restaurant_id: UUID
    delivery_partner_id: UUID | None
    status: DeliveryStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )