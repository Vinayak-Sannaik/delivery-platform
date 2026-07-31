from app.models.delivery_partner import DeliveryPartner
from app.repositories.delivery_partner_repository import (
    DeliveryPartnerRepository,
)
from app.schemas.delivery_partner import (
    CreateDeliveryPartnerRequest,
)


class DeliveryPartnerService:
    def __init__(
        self,
        delivery_partner_repository: DeliveryPartnerRepository,
    ):
        self.delivery_partner_repository = delivery_partner_repository

    async def create(
        self,
        request: CreateDeliveryPartnerRequest,
    ) -> DeliveryPartner:

        existing = (
            await self.delivery_partner_repository.get_by_user_id(
                request.user_id
            )
        )

        if existing:
            raise ValueError(
                "Delivery partner already exists"
            )

        partner = DeliveryPartner(
            user_id=request.user_id,
            is_available=True,
        )

        await self.delivery_partner_repository.create(
            partner
        )

        await self.delivery_partner_repository.db.commit()

        return partner