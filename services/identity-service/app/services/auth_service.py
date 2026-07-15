# from pwdlib import PasswordHash

# from app.models.user import User
# from app.repositories.user_repository import UserRepository
# from app.schemas.user import SignupRequest

# password_hash = PasswordHash.recommended()


# class AuthService:

#     def __init__(self, repo: UserRepository):
#         self.repo = repo

#     def signup(self, request: SignupRequest):

#         existing = self.repo.find_by_email(request.email)

#         if existing:
#             raise ValueError("Email already exists")

#         user = User(
#             email=request.email,
#             password_hash=password_hash.hash(request.password),
#             first_name=request.first_name,
#             last_name=request.last_name,
#             phone=request.phone,
#         )

#         return self.repo.create(user)
    

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import SignupRequest
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def signup(self, request: SignupRequest) -> User:

        existing = self.user_repository.find_by_email(request.email)

        if existing:
            raise ValueError("Email already exists")

        user = User(
            email=request.email,
            password_hash=password_hash.hash(request.password),
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