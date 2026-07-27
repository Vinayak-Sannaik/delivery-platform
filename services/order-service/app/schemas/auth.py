from uuid import UUID

from pydantic import BaseModel

from app.models.user import RoleEnum


class CurrentUser(BaseModel):
    user_id: UUID
    role: RoleEnum