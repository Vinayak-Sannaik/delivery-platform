from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import SignupRequest, SignupResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup", response_model=SignupResponse)
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    user = service.signup(request)

    return SignupResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )