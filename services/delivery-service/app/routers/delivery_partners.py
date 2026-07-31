from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.delivery_partner import (
    get_delivery_partner_service,
)
from app.schemas.delivery_partner import (
    CreateDeliveryPartnerRequest,
    DeliveryPartnerResponse,
)
from app.services.delivery_partner_service import (
    DeliveryPartnerService,
)

router = APIRouter(
    prefix="/delivery-partners",
    tags=["Delivery Partners"],
)


@router.post(
    "",
    response_model=DeliveryPartnerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_delivery_partner(
    request: CreateDeliveryPartnerRequest,
    service: DeliveryPartnerService = Depends(
        get_delivery_partner_service
    ),
):
    try:
        return await service.create(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )