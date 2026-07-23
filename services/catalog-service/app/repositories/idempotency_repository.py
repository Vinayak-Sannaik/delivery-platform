from sqlalchemy.orm import Session

from app.models.idempotency_key import IdempotencyKey


class IdempotencyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_key(self, key: str) -> IdempotencyKey | None:
        return (
            self.db.query(IdempotencyKey)
            .filter(IdempotencyKey.key == key)
            .first()
        )

    def create(
        self,
        idempotency_key: IdempotencyKey,
    ) -> IdempotencyKey:
        self.db.add(idempotency_key)
        self.db.commit()
        self.db.refresh(idempotency_key)
        return idempotency_key