
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RestaurantCreate(BaseModel):
    name: str
    description: str | None = None
    phone: str | None = None
    address: str | None = None
    image_url: str | None = None


class RestaurantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    phone: str | None = None
    address: str | None = None
    image_url: str | None = None
    is_active: bool | None = None


class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    name: str
    description: str | None
    phone: str | None
    address: str | None
    image_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime