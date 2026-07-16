from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.auth_service import AuthService

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:

    return AuthService(
        db=db,
        user_repository=UserRepository(db),
        refresh_token_repository=RefreshTokenRepository(db),
    )