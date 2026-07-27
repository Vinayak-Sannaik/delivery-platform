from app.models.status_enum import OrderStatus

VALID_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.PREPARING,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PREPARING: {
        OrderStatus.READY,
    },
    OrderStatus.READY: {
        OrderStatus.OUT_FOR_DELIVERY,
    },
    OrderStatus.OUT_FOR_DELIVERY: {
        OrderStatus.DELIVERED,
    },
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}


def is_valid_transition(
    current: OrderStatus,
    new: OrderStatus,
) -> bool:
    return new in VALID_TRANSITIONS[current]