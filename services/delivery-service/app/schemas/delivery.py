from pydantic import BaseModel

from app.models.delivery_status import DeliveryStatus


class UpdateDeliveryStatusRequest(BaseModel):
    status: DeliveryStatus