# id
# restaurant_id
# name
# created_at
# updated_at

from app.core.database import Base
import uuid
from sqlalchemy import DateTime, String, func, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.restaurant import Restaurant

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        UniqueConstraint(
            "restaurant_id",
            "name",
            name="uq_restaurant_category_name",
        ),
        Index(
            "ix_categories_restaurant_id",
            "restaurant_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('restaurants.id', ondelete="CASCADE"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="categories",
    )
