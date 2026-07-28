import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.order import Order
from app.models.status_enum import OrderStatus
from app.models.user import RoleEnum

from app.schemas.auth import CurrentUser

from app.dependencies.auth import get_current_user
from app.dependencies.order import get_order_service

from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.idempotency_repository import IdempotencyRepository
from app.services.outbox_service import OutboxService
from app.main import app


def build_mock_outbox_service():
    """Creates a mock OutboxService with async methods standard for event tracking."""
    outbox = AsyncMock(spec=OutboxService)
    outbox.create_order_created = AsyncMock()
    outbox.create_order_status_updated = AsyncMock()
    outbox.create_order_cancelled = AsyncMock()
    return outbox


@pytest.mark.asyncio
async def test_owner_can_update_own_restaurant_order(
    client,
    db_session,
):
    owner_id = uuid.uuid4()
    restaurant_id = uuid.uuid4()

    order = Order(
        customer_id=uuid.uuid4(),
        restaurant_id=restaurant_id,
        status=OrderStatus.PENDING,
        total_amount=Decimal("500.00"),
    )

    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    class FakeCatalogClient:
        async def get_restaurant_owner(self, restaurant_id):
            return str(owner_id)

    mock_outbox = build_mock_outbox_service()

    async def override_order_service():
        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            outbox_service=mock_outbox,
            catalog_client=FakeCatalogClient(),
            db=db_session,
        )

    def override_current_user():
        return CurrentUser(
            user_id=owner_id,
            role=RoleEnum.RESTAURANT_OWNER,
        )

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_order_service] = override_order_service

    response = await client.patch(
        f"/orders/{order.id}/status",
        json={"status": "CONFIRMED"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CONFIRMED"

    # Verify that the outbox status update event was emitted
    mock_outbox.create_order_status_updated.assert_called_once()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_owner_cannot_update_other_restaurant_order(
    client,
    db_session,
):
    owner_id = uuid.uuid4()
    another_owner_id = uuid.uuid4()
    restaurant_id = uuid.uuid4()

    order = Order(
        customer_id=uuid.uuid4(),
        restaurant_id=restaurant_id,
        status=OrderStatus.PENDING,
        total_amount=Decimal("500.00"),
    )

    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    class FakeCatalogClient:
        async def get_restaurant_owner(self, restaurant_id):
            return str(another_owner_id)

    mock_outbox = build_mock_outbox_service()

    async def override_order_service():
        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            outbox_service=mock_outbox,
            catalog_client=FakeCatalogClient(),
            db=db_session,
        )

    def override_current_user():
        return CurrentUser(
            user_id=owner_id,
            role=RoleEnum.RESTAURANT_OWNER,
        )

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_order_service] = override_order_service

    response = await client.patch(
        f"/orders/{order.id}/status",
        json={"status": "CONFIRMED"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only update orders from your own restaurant."
    )

    # Outbox should NOT be called on unauthorized request
    mock_outbox.create_order_status_updated.assert_not_called()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_admin_can_update_any_order(
    client,
    db_session,
):
    restaurant_id = uuid.uuid4()

    order = Order(
        customer_id=uuid.uuid4(),
        restaurant_id=restaurant_id,
        status=OrderStatus.PENDING,
        total_amount=Decimal("500.00"),
    )

    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    class FakeCatalogClient:
        async def get_restaurant_owner(self, restaurant_id):
            return str(uuid.uuid4())

    mock_outbox = build_mock_outbox_service()

    async def override_order_service():
        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            outbox_service=mock_outbox,
            catalog_client=FakeCatalogClient(),
            db=db_session,
        )

    def override_current_user():
        return CurrentUser(
            user_id=uuid.uuid4(),
            role=RoleEnum.ADMIN,
        )

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_order_service] = override_order_service

    response = await client.patch(
        f"/orders/{order.id}/status",
        json={"status": "CONFIRMED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED"

    # Verify that outbox event was triggered
    mock_outbox.create_order_status_updated.assert_called_once()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_customer_can_cancel_own_order(
    client,
    db_session,
):
    customer_id = uuid.uuid4()

    order = Order(
        customer_id=customer_id,
        restaurant_id=uuid.uuid4(),
        status=OrderStatus.PENDING,
        total_amount=Decimal("500.00"),
    )

    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    mock_outbox = build_mock_outbox_service()

    async def override_order_service():
        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            outbox_service=mock_outbox,
            catalog_client=None,
            db=db_session,
        )

    def override_current_user():
        return CurrentUser(
            user_id=customer_id,
            role=RoleEnum.CUSTOMER,
        )

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_order_service] = override_order_service

    response = await client.patch(
        f"/orders/{order.id}/cancel"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CANCELLED"

    # Verify cancellation outbox event was triggered
    mock_outbox.create_order_cancelled.assert_called_once()

    app.dependency_overrides.clear()