from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services.restaurant_service import RestaurantService
from app.schemas.auth import CurrentUser


from app.dependencies.services import get_restaurant_service
from app.dependencies.authorization import require_restaurant_owner

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=201,
)
def create_restaurant(
    request: Request,
    restaurant: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user: CurrentUser = Depends(require_restaurant_owner),
):
    owner_id = current_user.user_id

    return service.create(owner_id, restaurant, request=request,)


@router.get(
    "",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    name: str | None = None,
    is_active: bool | None = None,
    skip: int = 0,
    limit: int = 10,
    service: RestaurantService = Depends(get_restaurant_service),
):
    return service.get_all(name, is_active, skip, limit)


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: UUID,
    service: RestaurantService = Depends(get_restaurant_service),
):
    return service.get_by_id(restaurant_id)


@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def update_restaurant(
    restaurant_id: UUID,
    restaurant: RestaurantUpdate,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user: CurrentUser = Depends(require_restaurant_owner),
):
    return service.update(restaurant_id, restaurant, current_user)


@router.delete(
    "/{restaurant_id}",
    status_code=204,
)
def delete_restaurant(
    restaurant_id: UUID,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user: CurrentUser = Depends(require_restaurant_owner),
):
    service.delete(restaurant_id, current_user)