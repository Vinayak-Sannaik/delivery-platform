from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
        return self.db.scalar(stmt)
    
    def create(self, refresh_token: RefreshToken):
        self.db.add(refresh_token)
        return refresh_token