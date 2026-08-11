from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)

    event_type: str

    aggregate_id: UUID

    aggregate_type: str

    correlation_id: UUID

    causation_id: UUID | None = None

    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    version: int = 1

    data: dict[str, Any]