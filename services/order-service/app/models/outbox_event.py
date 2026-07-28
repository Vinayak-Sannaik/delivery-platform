# id

# aggregate_type

# aggregate_id

# event_type

# payload

# status

# created_at

# published_at
import uuid

from sqlalchemy import Enum as SQLEnum, String, DateTime, func,Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.outbox_event_status import OutboxEventStatus
from typing import Any
from datetime import datetime


class OutboxEvent(Base):
    __tablename__ = 'outbox_events'
    __table_args__ = (
        # Index("ix_outbox_status", "status"),
        # Index("ix_outbox_created_at", "created_at"),
        Index(
            "ix_outbox_status_created_at",
            "status",
            "created_at",
        ),
        {"schema": "orders"},
    )
        
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    aggregate_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    aggregate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    
    event_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    status: Mapped[OutboxEventStatus] = mapped_column(
        SQLEnum(
            OutboxEventStatus,
            name="outbox_event_status",
            schema="orders",
        ),
        nullable=False,
        default=OutboxEventStatus.PENDING,
    )
    
    payload: Mapped[dict[str, Any]] =  mapped_column(
        JSONB,
        nullable=False,
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    published_at: Mapped[DateTime | None ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
