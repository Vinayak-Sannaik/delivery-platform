from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.catalog_client import CatalogClient
from app.core.database import get_db
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService


async def get_order_service(
    db: AsyncSession,
) -> OrderService:

    order_repository = OrderRepository(db)
    order_item_repository = OrderItemRepository(db)
    catalog_client = CatalogClient()

    return OrderService(
        order_repository=order_repository,
        order_item_repository=order_item_repository,
        catalog_client=catalog_client,
        db=db,
    )