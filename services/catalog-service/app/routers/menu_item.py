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
    "/{menu_item_id}",
    response_model=MenuItemResponse,
)
def get_menu_item(
    menu_item_id: UUID,
    service: MenuItemService = Depends(get_menu_item_service),
):
    return service.get_by_id(menu_item_id)


# @router.get(
#     "/categories/{category_id}",
#     response_model=list[MenuItemResponse],
# )
# def list_menu_items(
#     category_id: UUID,
#     skip: int = Query(default=0, ge=0),
#     limit: int = Query(default=10, ge=1, le=100),
#     service: MenuItemService = Depends(get_menu_item_service),
# ):
#     return service.list_by_category(
#         category_id=category_id,
#         skip=skip,
#         limit=limit,
#     )


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
    