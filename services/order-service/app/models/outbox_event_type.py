from enum import Enum


class OutboxEventType(str, Enum):
    ORDER_CREATED = "OrderCreated"
    ORDER_STATUS_UPDATED = "OrderStatusUpdated"
    ORDER_CANCELLED = "OrderCancelled"