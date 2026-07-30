from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderItemEvent(BaseModel):
    menu_item_id: UUID
    item_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderCreatedEvent(BaseModel):
    order_id: UUID
    customer_id: UUID
    restaurant_id: UUID
    total_amount: Decimal
    status: str