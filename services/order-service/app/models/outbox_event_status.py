from enum import Enum


class OutboxEventStatus(Enum):
    PENDING = "pending"
    PUBLISHED = "published"