from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.schemas.menu_item import (
    UpdateMenuItem,
    MenuItemResponse,
)
from app.services.menu_item_service import MenuItemService
from app.dependencies.menu_item import get_menu_item_service

from app.schemas.auth import CurrentUser
from app.dependencies.authorization import require_restaurant_owner

from decimal import Decimal

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"],
)


# def get_menu_item_service(
#     db: Session = Depends(get_db),
# ) -> MenuItemService:
#     return MenuItemService(
#         category_repo=CategoryRepository(db),
#         menu_item_repo=MenuItemRepository(db),
#     )


# @router.post(
#     "/categories/{category_id}",
#     response_model=MenuItemResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_menu_item(
#     category_id: UUID,
#     menu_item: CreateMenuItem,
#     service: MenuItemService = Depends(get_menu_item_service),
# ):
#     return service.create(
#         category_id=category_id,
#         menu_item_data=menu_item,
#     )




@router.get(
    "/search",
    response_model=list[MenuItemResponse],
)
def search_menu_items(
    name: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    is_available: bool | None = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: MenuItemService = Depends(get_menu_item_service),
):
    
    return service.search(
        name=name,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/{menu_item_id}",
    response_model=MenuItemResponse,
)
def get_menu_item(
    menu_item_id: UUID,
    service: MenuItemService = Depends(get_menu_item_service),
):
    return service.get_by_id(menu_item_id)


@router.put(
    "/{menu_item_id}",
    response_model=MenuItemResponse,
)
def update_menu_item(
    menu_item_id: UUID,
    menu_item: UpdateMenuItem,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: CurrentUser = Depends(require_restaurant_owner),
):
    return service.update(
        menu_item_id=menu_item_id,
        menu_item_data=menu_item,
        current_user=current_user,
    )


@router.delete(
    "/{menu_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_menu_item(
    menu_item_id: UUID,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: CurrentUser = Depends(require_restaurant_owner)
):
    service.delete(menu_item_id, current_user)
    