from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.catalog_client import CatalogClient
from app.clients.catalog_http_client import CatalogHttpClient
from app.core.config import settings
from app.core.database import get_db
from app.repositories.idempotency_repository import IdempotencyRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.outbox_repository import OutboxRepository
from app.services.order_service import OrderService
from app.services.outbox_service import OutboxService


def get_catalog_http_client(
    request: Request,
) -> CatalogHttpClient:
    return request.app.state.catalog_client

    # Application
    #   │
    #   ├── CatalogHttpClient
    #   │        │
    #   │        └── AsyncClient (single connection pool)
    #   │
    # Request 1 ─────┘
    # Request 2 ─────┘
    # Request 3 ─────┘


async def get_order_service(
    request: Request,
    db: AsyncSession = Depends(get_db),
    catalog_http_client: CatalogHttpClient = Depends(get_catalog_http_client),
) -> OrderService:

    order_repository = OrderRepository(db)
    order_item_repository = OrderItemRepository(db)
    idempotency_repository = IdempotencyRepository(db)
    outbox_repository = OutboxRepository(db)


    # After introducing OutboxService, OrderService should never talk to the repository. It should only know about the service.
    outbox_service = OutboxService(
        outbox_repository=outbox_repository,
    )

    if settings.CATALOG_MODE == "http":
        catalog_client = catalog_http_client
    else:
        catalog_client = CatalogClient()

    return OrderService(
        order_repository=order_repository,
        order_item_repository=order_item_repository,
        catalog_client=catalog_client,
        idempotency_repository=idempotency_repository,
        outbox_service=outbox_service,
        db=db,
    )