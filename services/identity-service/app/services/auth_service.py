
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import SignupRequest, LoginRequest, LoginResponse
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.security.password import verify_password, hash_password, hash_refresh_token
from app.security.jwt import create_access_token, create_refresh_token
from app.core.config import settings
from app.exceptions.InvalidCredentialsException import InvalidCredentialsException
from pwdlib import PasswordHash 

from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.models.refresh_token import RefreshToken

password_hash = PasswordHash.recommended()


class AuthService:

    def __init__(
            self, 
            db: Session, 
            user_repository: UserRepository,
            refresh_token_repository: RefreshTokenRepository
            ):
        self.db = db
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    def signup(self, request: SignupRequest) -> User:

        existing = self.user_repository.find_by_email(request.email)

        if existing:
            raise ValueError("Email already exists")

        user = User(
            email=request.email,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
        )

        try:
            self.user_repository.create(user)

            self.db.commit()

            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()
            raise

        except Exception:
            self.db.rollback()
            raise



    def login(self, request: LoginRequest) -> LoginResponse:

        user = self.user_repository.find_by_email(request.email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()

        access_token = create_access_token(str(user.id), user.role)

        refresh_token, jti = create_refresh_token(str(user.id))

        refresh = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=datetime.now(UTC)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        self.refresh_token_repository.create(refresh)

        self.db.commit()

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )