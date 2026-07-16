from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.timestamp_mixin import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(TimestampMixin, Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    jti: Mapped[UUID] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")