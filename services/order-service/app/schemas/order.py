# app/schemas/order.py

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.status_enum import OrderStatus


class CreateOrderItemRequest(BaseModel):
    menu_item_id: UUID
    quantity: int = Field(..., ge=1)


class CreateOrderRequest(BaseModel):
    items: list[CreateOrderItemRequest] = Field(..., min_length=1)


class UpdateOrderRequest(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    menu_item_id: UUID
    item_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    restaurant_id: UUID
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]