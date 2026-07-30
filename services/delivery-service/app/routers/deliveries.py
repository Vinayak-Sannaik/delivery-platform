from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.delivery import get_delivery_service
from app.services.delivery_service import DeliveryService
from app.schemas.delivery import UpdateDeliveryStatusRequest
from fastapi import status


router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
)


@router.get("/{order_id}")
async def get_delivery(
    order_id: UUID,
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.get_by_order_id(order_id)


@router.patch(
    "/{order_id}/status",
)
async def update_delivery_status(
    order_id: UUID,
    request: UpdateDeliveryStatusRequest,
    service: DeliveryService = Depends(get_delivery_service),
):
    return await service.update_status(
        order_id=order_id,
        status=request.status,
    )