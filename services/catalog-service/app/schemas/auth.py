from pydantic import BaseModel, Field
from uuid import UUID

class CurrentUser(BaseModel):
    user_id: UUID
    role: str | None = None