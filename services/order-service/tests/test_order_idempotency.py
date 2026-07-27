import uuid

import pytest

from app.dependencies.auth import get_current_user
from app.dependencies.order import get_order_service

from app.main import app
from app.models.user import RoleEnum
from app.schemas.auth import CurrentUser

from app.repositories.idempotency_repository import IdempotencyRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService


@pytest.mark.asyncio
async def test_same_idempotency_key_returns_same_order(
    client,
    db_session,
):

    customer_id = uuid.uuid4()
    restaurant_id = uuid.uuid4()
    menu_item_id = uuid.uuid4()


    class FakeMenuItem:

        def __init__(self):
            self.id = str(menu_item_id)
            self.restaurant_id = str(restaurant_id)
            self.name = "Burger"
            self.price = "100.00"
            self.is_available = True


    class FakeCatalogClient:

        async def get_menu_items(
            self,
            menu_item_ids,
        ):
            return [FakeMenuItem()]


    async def override_order_service():

        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            catalog_client=FakeCatalogClient(),
            db=db_session,
        )


    def override_current_user():

        return CurrentUser(
            user_id=customer_id,
            role=RoleEnum.CUSTOMER,
        )


    app.dependency_overrides[
        get_current_user
    ] = override_current_user

    app.dependency_overrides[
        get_order_service
    ] = override_order_service


    payload = {
        "items": [
            {
                "menu_item_id": str(menu_item_id),
                "quantity": 2,
            }
        ]
    }


    response1 = await client.post(
        "/orders",
        json=payload,
        headers={
            "Idempotency-Key": "order-123",
        },
    )


    response2 = await client.post(
        "/orders",
        json=payload,
        headers={
            "Idempotency-Key": "order-123",
        },
    )


    assert response1.status_code == 201
    assert response2.status_code == 201

    assert (
        response1.json()["id"]
        == response2.json()["id"]
    )

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_different_idempotency_key_creates_new_order(
    client,
    db_session,
):

    customer_id = uuid.uuid4()
    restaurant_id = uuid.uuid4()
    menu_item_id = uuid.uuid4()


    class FakeMenuItem:

        def __init__(self):
            self.id = str(menu_item_id)
            self.restaurant_id = str(restaurant_id)
            self.name = "Burger"
            self.price = "100.00"
            self.is_available = True


    class FakeCatalogClient:

        async def get_menu_items(
            self,
            menu_item_ids,
        ):
            return [FakeMenuItem()]


    async def override_order_service():

        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            catalog_client=FakeCatalogClient(),
            db=db_session,
        )


    def override_current_user():

        return CurrentUser(
            user_id=customer_id,
            role=RoleEnum.CUSTOMER,
        )


    app.dependency_overrides[
        get_current_user
    ] = override_current_user

    app.dependency_overrides[
        get_order_service
    ] = override_order_service


    payload = {
        "items": [
            {
                "menu_item_id": str(menu_item_id),
                "quantity": 1,
            }
        ]
    }


    response1 = await client.post(
        "/orders",
        json=payload,
        headers={
            "Idempotency-Key": "key-1",
        },
    )


    response2 = await client.post(
        "/orders",
        json=payload,
        headers={
            "Idempotency-Key": "key-2",
        },
    )


    assert response1.status_code == 201
    assert response2.status_code == 201

    assert (
        response1.json()["id"]
        != response2.json()["id"]
    )

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_same_key_different_customer_returns_conflict(
    client,
    db_session,
):

    restaurant_id = uuid.uuid4()
    menu_item_id = uuid.uuid4()


    class FakeMenuItem:

        def __init__(self):
            self.id = str(menu_item_id)
            self.restaurant_id = str(restaurant_id)
            self.name = "Burger"
            self.price = "100.00"
            self.is_available = True


    class FakeCatalogClient:

        async def get_menu_items(
            self,
            menu_item_ids,
        ):
            return [FakeMenuItem()]


    async def override_order_service():

        return OrderService(
            order_repository=OrderRepository(db_session),
            order_item_repository=OrderItemRepository(db_session),
            idempotency_repository=IdempotencyRepository(db_session),
            catalog_client=FakeCatalogClient(),
            db=db_session,
        )


    customer_one = uuid.uuid4()
    customer_two = uuid.uuid4()


    def current_user_one():

        return CurrentUser(
            user_id=customer_one,
            role=RoleEnum.CUSTOMER,
        )


    def current_user_two():

        return CurrentUser(
            user_id=customer_two,
            role=RoleEnum.CUSTOMER,
        )


    app.dependency_overrides[
        get_order_service
    ] = override_order_service


    payload = {
        "items": [
            {
                "menu_item_id": str(menu_item_id),
                "quantity": 1,
            }
        ]
    }


    app.dependency_overrides[
        get_current_user
    ] = current_user_one

    response1 = await client.post(
        "/orders",
        json=payload,
        headers={
            "Idempotency-Key": "shared-key",
        },
    )


    app.dependency_overrides[
        get_current_user
    ] = current_user_two

    response2 = await client.post(
        "/orders",
        json=payload,
        headers={
            "Idempotency-Key": "shared-key",
        },
    )


    assert response1.status_code == 201
    assert response2.status_code == 409

    assert (
        response2.json()["detail"]
        == "Idempotency key already used by another customer."
    )

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_missing_idempotency_key_returns_422(
    client,
    db_session,
):
    customer_id = uuid.uuid4()

    def override_current_user():
        return CurrentUser(
            user_id=customer_id,
            role=RoleEnum.CUSTOMER,
        )

    app.dependency_overrides[
        get_current_user
    ] = override_current_user

    response = await client.post(
        "/orders",
        json={
            "items": [
                {
                    "menu_item_id": str(uuid.uuid4()),
                    "quantity": 1,
                }
            ]
        },
    )

    assert response.status_code == 422

    app.dependency_overrides.clear()