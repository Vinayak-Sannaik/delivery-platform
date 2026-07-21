from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal


class CreateMenuItem(BaseModel):
    name: str = Field(min_length = 1, max_length = 255)
    price: Decimal
    description: str |  None = None
    is_available: bool = True

class UpdateMenuItem(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    price: Decimal | None = None
    description: str | None = None
    is_available: bool | None = None
    
class MenuItemResponse(CreateMenuItem):
    id: UUID
    model_config = {
        "from_attributes": True
    }




