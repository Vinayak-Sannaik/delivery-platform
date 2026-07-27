from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class MenuItemDto(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    price: Decimal
    is_available: bool