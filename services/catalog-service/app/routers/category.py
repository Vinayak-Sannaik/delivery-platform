from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.category import get_category_service
from app.dependencies.menu_item import get_menu_item_service
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.menu_item import (
    CreateMenuItem,
    MenuItemResponse
)
from app.services.category_service import CategoryService
from app.services.menu_item_service import MenuItemService

from app.schemas.auth import CurrentUser
from app.dependencies.authorization import require_restaurant_owner

from decimal import Decimal

router = APIRouter(
    prefix="",
    tags=["Categories"],
)


@router.post(
    "/{category_id}/menu_items",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item(
    category_id: UUID,
    menu_item: CreateMenuItem,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: CurrentUser = Depends(require_restaurant_owner),
):
    return service.create(
        category_id=category_id,
        menu_item_data=menu_item,
        current_user=current_user
    )
    
@router.get(
    "/{category_id}/menu_items",
    response_model=list[MenuItemResponse],
)
def list_menu_items(
    category_id: UUID,
    name : str | None = None,
    is_available : bool | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    service: MenuItemService = Depends(get_menu_item_service),
):
    return service.list_by_category(
        category_id=category_id,
        name = name,
        is_available = is_available,
        min_price = min_price,
        max_price = max_price,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/restaurants/{restaurant_id}/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    restaurant_id: UUID,
    category_data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    current_user: CurrentUser = Depends(require_restaurant_owner),
):
    return service.create(
        restaurant_id=restaurant_id,
        category_data=category_data,
        current_user=current_user
    )


@router.get(
    "/restaurants/{restaurant_id}/categories",
    response_model=list[CategoryResponse],
)
def list_categories(
    restaurant_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return service.list_by_restaurant(
        restaurant_id=restaurant_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
):
    return service.get_by_id(category_id)


@router.put(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return service.update(
        category_id=category_id,
        category_data=category_data,
    )


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
):
    service.delete(category_id)