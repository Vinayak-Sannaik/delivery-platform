from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.dependencies.delivery import get_delivery_service
from app.services.delivery_service import DeliveryService
from app.schemas.delivery import UpdateDeliveryStatusRequest
from fastapi import status

from app.dependencies.auth import get_current_user
from app.schemas.auth import CurrentUser

from app.schemas.delivery import AssignDeliveryPartnerRequest

from app.schemas.delivery import DeliveryResponse

router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
)

@router.get(
    "/me",
    response_model=list[DeliveryResponse],
)
async def get_my_deliveries(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.get_my_deliveries(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )


@router.get("/{order_id}", response_model=DeliveryResponse,)
async def get_delivery(
    order_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.get_by_order_id(order_id, current_user)


@router.patch(
    "/{order_id}/status",
    response_model=DeliveryResponse,
)
async def update_delivery_status(
    order_id: UUID,
    request: UpdateDeliveryStatusRequest,
    current_user: CurrentUser = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.update_status(
        order_id=order_id,
        status=request.status,
        current_user=current_user,
    )
    

@router.patch("/{order_id}/assign", response_model=DeliveryResponse,)
async def assign_delivery_partner(
    order_id: UUID,
    request: AssignDeliveryPartnerRequest,
    current_user: CurrentUser = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.assign_partner(
        order_id=order_id,
        delivery_partner_id=request.delivery_partner_id,
        current_user=current_user,
    )
    

@router.patch(
    "/{order_id}/cancel",
    response_model=DeliveryResponse,
)
async def cancel_delivery(
    order_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.cancel_delivery(
        order_id=order_id,
        current_user=current_user,
    )
    
    
    
@router.get(
    "/deliveries",
    response_model=list[DeliveryResponse],
)
async def get_all_deliveries(
    current_user: CurrentUser = Depends(get_current_user),
    service: DeliveryService = Depends(get_delivery_service),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    return await service.get_all(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )