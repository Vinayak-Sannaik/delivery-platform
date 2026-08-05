from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status

from app.clients.catalog_client import CatalogClient
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.schemas.order import CreateOrderRequest
from app.repositories.order_item_repository import OrderItemRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import RoleEnum
from app.schemas.auth import CurrentUser
from app.schemas.order import UpdateOrderRequest
from app.services.order_status_service import is_valid_transition
from app.models.status_enum import OrderStatus
from app.repositories.idempotency_repository import IdempotencyRepository
from app.services.outbox_service import OutboxService

from app.models.status_enum import OrderStatus

class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        catalog_client: CatalogClient,
        idempotency_repository: IdempotencyRepository,
        
        outbox_service: OutboxService,
    
        db: AsyncSession
    ):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository
        self.catalog_client = catalog_client
        self.idempotency_repository = idempotency_repository
        self.outbox_service = outbox_service
        self.db = db

    async def create(
        self,
        request: CreateOrderRequest,
        customer_id: UUID,
        idempotency_key: str,
    ) -> Order:
        
        existing = await self.idempotency_repository.get_by_key(
            idempotency_key
        )

        if existing:
            if existing.customer_id != customer_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Idempotency key already used by another customer.",
                )

            order = await self.order_repository.get_by_id(
                existing.order_id
            )

            return order

        menu_item_ids = [
            item.menu_item_id
            for item in request.items
        ]

        menu_items = await self.catalog_client.get_menu_items(
            menu_item_ids
        )

        if len(menu_items) != len(menu_item_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more menu items do not exist.",
            )

        menu_item_map = {
            UUID(item.id): item
            for item in menu_items
        }

        restaurant_id = None
        total_amount = Decimal("0.00")
        order_items = []

        for request_item in request.items:

            menu_item = menu_item_map.get(
                request_item.menu_item_id
            )

            if menu_item is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Menu item not found.",
                )

            if not menu_item.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{menu_item.name} is unavailable.",
                )

            if restaurant_id is None:
                restaurant_id = UUID(menu_item.restaurant_id)

            elif restaurant_id != UUID(menu_item.restaurant_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="All menu items must belong to the same restaurant.",
                )

            subtotal = (
                Decimal(str(menu_item.price))
                * request_item.quantity
            )

            total_amount += subtotal

            order_items.append(
                OrderItem(
                    menu_item_id=request_item.menu_item_id,
                    item_name=menu_item.name,
                    quantity=request_item.quantity,
                    unit_price=Decimal(str(menu_item.price)),
                    subtotal=subtotal,
                )
            )

        order = Order(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            total_amount=total_amount,
        )

        try:
            await self.order_repository.create(order)

            for item in order_items:
                item.order_id = order.id

            await self.order_item_repository.create_many(order_items)

            await self.idempotency_repository.create(
                key=idempotency_key,
                customer_id=customer_id,
                order_id=order.id,
            )
            
            await self.outbox_service.create_order_created(order)

            await self.db.commit()

            order = await self.order_repository.get_by_id(
                order.id
            )

            return order

        except Exception:
            await self.db.rollback()
            raise


    async def get_by_id(
        self,
        order_id: UUID,
        current_user: CurrentUser,
    ) -> Order:

        order = await self.order_repository.get_by_id(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        if (
            current_user.role != RoleEnum.ADMIN
            and order.customer_id != current_user.user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized.",
            )

        return order
    
    
    async def get_by_customer(
        self,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Order]:
        return await self.order_repository.get_by_customer(
            customer_id=current_user.user_id,
            skip=skip,
            limit=limit,
        )
        
    async def get_by_restaurant(
        self,
        restaurant_id: UUID,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Order]:

        restaurant = await self.catalog_client.get_restaurant_owner(
            str(restaurant_id)
        )
        
        print("Restaurant owner_id:", restaurant["owner_id"])
        print("Current user_id:", current_user.user_id)

        if restaurant["owner_id"] != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to view these orders.",
            )

        return await self.order_repository.get_by_restaurant(
            restaurant_id=restaurant_id,
            skip=skip,
            limit=limit,
        )
        
    async def update_status(
        self,
        order_id: UUID,
        request: UpdateOrderRequest,
        current_user: CurrentUser,
    ) -> Order:

        order = await self.order_repository.get_by_id(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        # Validate state transition
        if not is_valid_transition(
            order.status,
            request.status,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Cannot change order status from "
                    f"{order.status.value} to {request.status.value}."
                ),
            )

        # Role-based authorization
        match current_user.role:

            case RoleEnum.ADMIN:
                pass

            case RoleEnum.RESTAURANT_OWNER:
                owner_id = await self.catalog_client.get_restaurant_owner(
                    order.restaurant_id
                )

                if owner_id != str(current_user.user_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You can only update orders from your own restaurant.",
                    )

                allowed_statuses = {
                    OrderStatus.CONFIRMED,
                    OrderStatus.PREPARING,
                    OrderStatus.READY,
                }

                if request.status not in allowed_statuses:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Restaurant owner is not allowed to perform this action.",
                    )

            case RoleEnum.DELIVERY_PARTNER:
                allowed_statuses = {
                    OrderStatus.OUT_FOR_DELIVERY,
                    OrderStatus.DELIVERED,
                }

                if request.status not in allowed_statuses:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Delivery partner is not allowed to perform this action.",
                    )

            case RoleEnum.CUSTOMER:
                if request.status != OrderStatus.CANCELLED:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Customer can only cancel an order.",
                    )

            case _:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to update this order.",
                )

        order.status = request.status

        await self.order_repository.update(order)
        
        await self.outbox_service.create_order_status_updated(order)

        await self.db.commit()

        order = await self.order_repository.get_by_id(
            order.id
        )

        return order
    
    
    async def cancel(
        self,
        order_id: UUID,
        current_user: CurrentUser,
    ) -> Order:

        order = await self.order_repository.get_by_id(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        if order.customer_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own orders.",
            )

        if order.status not in (
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order can no longer be cancelled.",
            )

        order.status = OrderStatus.CANCELLED

        await self.order_repository.update(order)
        
        await self.outbox_service.create_order_cancelled(order)

        await self.db.commit()

        order = await self.order_repository.get_by_id(
            order.id
        )

        return order