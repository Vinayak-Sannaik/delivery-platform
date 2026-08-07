from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from app.models.user import RoleEnum
from enum import Enum
class SignupRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=10, max_length=20)
    role: SignupRole = SignupRole.CUSTOMER


class SignupResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleEnum

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    
class CurrentUserResponse(BaseModel):
    id: UUID
    email: str
    role: RoleEnum

    model_config = {
        "from_attributes": True,
    }