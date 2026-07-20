from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    restaurant_id: UUID




