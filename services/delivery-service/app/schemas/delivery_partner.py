from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateDeliveryPartnerRequest(BaseModel):
    user_id: UUID


class DeliveryPartnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    is_available: bool
    created_at: datetime
    updated_at: datetime