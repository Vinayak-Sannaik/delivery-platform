import uuid

from sqlalchemy import (
    String,
    DateTime,
    func,
    Index,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class IdempotencyKey(Base):

    __tablename__ = "idempotency_keys"

    __table_args__ = (
        Index(
            "ix_idempotency_keys_key",
            "key",
        ),
        Index(
            "ix_idempotency_keys_order_id",
            "order_id",
        ),
        {
            "schema": "orders"
        },
    )


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


    key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )


    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )


    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "orders.orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )


    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )