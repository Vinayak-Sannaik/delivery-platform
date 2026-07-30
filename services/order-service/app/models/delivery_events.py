from enum import Enum


class DeliveryEventType(str, Enum):
    DELIVERY_ASSIGNED = "DeliveryAssigned"
    DELIVERY_CANCELLED = "DeliveryCancelled"
    DELIVERY_STATUS_CHANGED = "DeliveryStatusChanged"