from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.catalog_client import CatalogClient
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService
from app.repositories.idempotency_repository import IdempotencyRepository


from fastapi import Depends
from app.core.database import get_db


async def get_order_service(
    db: AsyncSession = Depends(get_db),
) -> OrderService:

    order_repository = OrderRepository(db)
    order_item_repository = OrderItemRepository(db)
    catalog_client = CatalogClient()
    idempotency_repository = IdempotencyRepository(db)

    return OrderService(
        order_repository=order_repository,
        order_item_repository=order_item_repository,
        catalog_client=catalog_client,
        idempotency_repository=idempotency_repository,
        db=db,
    )