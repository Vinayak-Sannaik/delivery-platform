from uuid import UUID
from decimal import Decimal
import json

from fastapi import HTTPException, status

from app.models.menu_item import MenuItem
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.schemas.menu_item import CreateMenuItem, UpdateMenuItem
from app.schemas.auth import CurrentUser
from app.services.authorization_service import AuthorizationService

from app.schemas.menu_item import CreateMenuItem, UpdateMenuItem,  MenuItemResponse
from app.core.redis import redis_client,  get_menu_item_cache_key,  get_menu_items_list_cache_key, invalidate_menu_items_cache,  MENU_ITEM_CACHE_TTL

class MenuItemService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        menu_item_repo: MenuItemRepository,
        authorization_service: AuthorizationService
    ):
        self.category_repo = category_repo
        self.menu_item_repo = menu_item_repo
        self.authorization_service = authorization_service

    # def _authorize_restaurant_owner(
    #     self,
    #     restaurant: Restaurant,
    #     current_user: CurrentUser,
    # ) -> None:
    #     # Admin can manage every restaurant
    #     if current_user.role == RoleEnum.ADMIN:
    #         return

    #     # Restaurant owner can manage only their own restaurant
    #     if restaurant.owner_id == current_user.user_id:
    #         return

    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You are not authorized to perform this action on this restaurant.",
    #     )

    def create(
        self,
        category_id: UUID,
        menu_item_data: CreateMenuItem,
        current_user: CurrentUser,
    ) -> MenuItem:

        category = self.category_repo.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        self.authorization_service.authorize_restaurant_owner(
            category.restaurant,
            current_user,
        )
        existing_menu_item = self.menu_item_repo.get_by_category_and_name(
            category_id=category_id,
            name=menu_item_data.name,
        )

        if existing_menu_item:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Menu item already exists.",
            )

        menu_item = MenuItem(
            category_id=category_id,
            name=menu_item_data.name,
            description=menu_item_data.description,
            price=menu_item_data.price,
            is_available=menu_item_data.is_available,
        )

        created_menu_item = self.menu_item_repo.create(
            menu_item
        )

        invalidate_menu_items_cache(
            str(category_id)
        )

        return created_menu_item

    def get_by_id(
        self,
        menu_item_id: UUID,
    ) -> MenuItemResponse:

        cache_key = get_menu_item_cache_key(
            str(menu_item_id)
        )

        # -----------------------------
        # Redis HIT
        # -----------------------------
        cached = redis_client.get(cache_key)

        if cached:
            print("FROM CACHE")
            return MenuItemResponse.model_validate_json(
                cached
            )

        # -----------------------------
        # Redis MISS
        # -----------------------------
        menu_item = self.menu_item_repo.get_by_id(
            menu_item_id
        )
        print("FROM DB")

        if menu_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found.",
            )

        response = MenuItemResponse.model_validate(
            menu_item,
            from_attributes=True,
        )

        # -----------------------------
        # Store in Redis
        # -----------------------------
        redis_client.setex(
            cache_key,
            MENU_ITEM_CACHE_TTL,
            response.model_dump_json(),
        )

        return response

    def list_by_category(
        self,
        category_id: UUID,
        name: str | None = None,
        is_available: bool | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[MenuItemResponse]:

        category = self.category_repo.get_by_id(
            category_id
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        cache_key = get_menu_items_list_cache_key(
            category_id=str(category_id),
            name=name,
            is_available=is_available,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit,
        )

        # -----------------------------
        # Redis HIT
        # -----------------------------
        cached = redis_client.get(cache_key)

        if cached:
            return [
                MenuItemResponse.model_validate(item)
                for item in json.loads(cached)
            ]

        # -----------------------------
        # Redis MISS
        # -----------------------------
        menu_items = self.menu_item_repo.get_all(
            category_id=category_id,
            name=name,
            is_available=is_available,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit,
        )

        response = [
            MenuItemResponse.model_validate(
                item,
                from_attributes=True,
            )
            for item in menu_items
        ]

        # -----------------------------
        # Redis SET
        # -----------------------------
        redis_client.setex(
            cache_key,
            MENU_ITEM_CACHE_TTL,
            json.dumps(
                [
                    item.model_dump(mode="json")
                    for item in response
                ]
            ),
        )

        return response

    def update(
        self,
        menu_item_id: UUID,
        menu_item_data: UpdateMenuItem,
        current_user: CurrentUser,
    ) -> MenuItem:

        menu_item = self._get_by_id_from_database(
            menu_item_id
        )

        self.authorization_service.authorize_restaurant_owner(
            menu_item.category.restaurant,
            current_user,
        )

        if (
            menu_item_data.name
            and menu_item_data.name != menu_item.name
        ):
            existing_menu_item = (
                self.menu_item_repo.get_by_category_and_name(
                    category_id=menu_item.category_id,
                    name=menu_item_data.name,
                )
            )

            if existing_menu_item:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Menu item already exists.",
                )

        update_data = menu_item_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(menu_item, key, value)

        updated_menu_item = self.menu_item_repo.update(
            menu_item
        )

        # Invalidate individual menu item cache
        redis_client.delete(
            get_menu_item_cache_key(
                str(menu_item_id)
            )
        )

        # Invalidate category menu item list caches
        invalidate_menu_items_cache(
            str(menu_item.category_id)
        )

        return updated_menu_item

    def delete(
        self,
        menu_item_id: UUID,
        current_user: CurrentUser,
    ) -> None:

        menu_item = self._get_by_id_from_database(
            menu_item_id
        )
        self.authorization_service.authorize_restaurant_owner(
            menu_item.category.restaurant,
            current_user,
        )
        category_id = menu_item.category_id

        self.menu_item_repo.delete(
            menu_item
        )

        redis_client.delete(
            get_menu_item_cache_key(
                str(menu_item_id)
            )
        )

        invalidate_menu_items_cache(
            str(category_id)
        )

    def get_menu_items_by_ids(
        self,
        menu_item_ids: list[UUID],
    ) -> list[MenuItem]:
        return self.menu_item_repo.get_by_ids(menu_item_ids)

    def _get_by_id_from_database(
        self,
        menu_item_id: UUID,
    ) -> MenuItem:
        menu_item = self.menu_item_repo.get_by_id(
            menu_item_id
        )

        if menu_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found.",
            )

        return menu_item

    def search(
        self,
        name: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        is_available: bool | None = True,
        skip: int = 0,
        limit: int = 20,
    ) -> list[MenuItemResponse]:

        menu_items = self.menu_item_repo.search_ai(
            name=name,
            min_price=min_price,
            max_price=max_price,
            is_available=is_available,
            skip=skip,
            limit=limit,
        )

        return [
            MenuItemResponse.model_validate(
                item,
                from_attributes=True,
            )
            for item in menu_items
        ]
