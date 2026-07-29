from uuid import UUID

import grpc
from fastapi import HTTPException

from app.core.database import SessionLocal
from app.grpc import catalog_pb2
from app.grpc import catalog_pb2_grpc
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.idempotency_repository import IdempotencyRepository
from app.services.authorization_service import AuthorizationService
from app.services.menu_item_service import MenuItemService
from app.services.restaurant_service import RestaurantService


class CatalogServiceServicer(catalog_pb2_grpc.CatalogServiceServicer):

    async def GetMenuItems(self, request, context):
        db = SessionLocal()

        try:
            category_repo = CategoryRepository(db)
            menu_item_repo = MenuItemRepository(db)
            authorization_service = AuthorizationService()

            menu_item_service = MenuItemService(
                category_repo=category_repo,
                menu_item_repo=menu_item_repo,
                authorization_service=authorization_service,
            )

            menu_item_ids = [
                UUID(item_id)
                for item_id in request.menu_item_ids
            ]

            menu_items = menu_item_service.get_menu_items_by_ids(
                menu_item_ids
            )

            return catalog_pb2.GetMenuItemsResponse(
                menu_items=[
                    catalog_pb2.MenuItem(
                        id=str(item.id),
                        restaurant_id=str(item.category.restaurant_id),
                        name=item.name,
                        price=str(item.price),
                        is_available=item.is_available,
                    )
                    for item in menu_items
                ]
            )

        finally:
            db.close()

    async def GetRestaurantOwner(self, request, context):
        db = SessionLocal()

        try:
            restaurant_repo = RestaurantRepository(db)
            idempotency_repo = IdempotencyRepository(db)
            authorization_service = AuthorizationService()

            restaurant_service = RestaurantService(
                repository=restaurant_repo,
                authorization_service=authorization_service,
                idempotency_repository=idempotency_repo,
            )

            try:
                restaurant = restaurant_service.get_by_id(
                    UUID(request.restaurant_id)
                )
            except HTTPException:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Restaurant not found.")
                return catalog_pb2.GetRestaurantOwnerResponse()

            return catalog_pb2.GetRestaurantOwnerResponse(
                owner_id=str(restaurant.owner_id)
            )

        finally:
            db.close()