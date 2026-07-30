from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.order import get_order_service
from app.schemas.auth import CurrentUser
from app.schemas.order import CreateOrderRequest, OrderResponse
from app.services.order_service import OrderService
from app.dependencies.auth import get_current_user
from uuid import UUID
from fastapi import Depends, Query
from app.schemas.order import UpdateOrderRequest

from fastapi import Header

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    request: CreateOrderRequest,
    idempotency_key: str = Header(...),
    current_user: CurrentUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.create(
        request=request,
        customer_id=current_user.user_id,
        idempotency_key=idempotency_key
    )
    
@router.get(
    "/me",
    response_model=list[OrderResponse],
)
async def get_my_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.get_by_customer(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
async def get_order(
    order_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.get_by_id(
        order_id,
        current_user,
    )
    
    
@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: UUID,
    request: UpdateOrderRequest,
    current_user: CurrentUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.update_status(
        order_id=order_id,
        request=request,
        current_user=current_user,
    )
    
@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
async def cancel_order(
    order_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.cancel(
        order_id=order_id,
        current_user=current_user,
    )