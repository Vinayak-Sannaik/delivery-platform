from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies.database import get_db
from sqlalchemy.orm import Session

from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository


router = APIRouter(
    prefix="/internal",
    tags=["Internal"],
)


class InternalMenuItemsRequest(BaseModel):
    menu_item_ids: list[UUID]
    

@router.get("/restaurants/{restaurant_id}/owner")
def get_internal_restaurant_owner(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
):
    repository = RestaurantRepository(db)

    restaurant = repository.get_by_id(
        restaurant_id
    )

    if not restaurant:
        return {
            "owner_id": None
        }

    return {
        "owner_id": str(restaurant.owner_id)
    }

@router.post("/menu-items")
def get_internal_menu_items(
    request: InternalMenuItemsRequest,
    db: Session = Depends(get_db),
):
    repository = MenuItemRepository(db)

    items = repository.get_by_ids(
        request.menu_item_ids
    )

    return [
        {
            "id": str(item.id),
            "restaurant_id": str(item.category.restaurant_id),
            "name": item.name,
            "price": float(item.price),
            "is_available": item.is_available,
        }
        for item in items
    ]