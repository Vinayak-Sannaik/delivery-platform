from fastapi import APIRouter, Depends

from app.dependencies.services import get_auth_service 

from app.schemas.user import SignupRequest, SignupResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


from fastapi import Depends

@router.post("/signup", response_model=SignupResponse)
def signup(
    request: SignupRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = service.signup(request)

    return SignupResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )