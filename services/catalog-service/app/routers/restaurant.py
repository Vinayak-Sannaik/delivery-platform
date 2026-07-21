from uuid import UUID

from fastapi import APIRouter, Depends
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
from app.dependencies.auth import get_current_user

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
    restaurant: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user: CurrentUser = Depends(get_current_user),
):
    owner_id = current_user.user_id

    return service.create(owner_id, restaurant)


@router.get(
    "",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    skip: int = 0,
    limit: int = 10,
    service: RestaurantService = Depends(get_restaurant_service),
):
    return service.get_all(skip, limit)


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
):
    return service.update(restaurant_id, restaurant)


@router.delete(
    "/{restaurant_id}",
    status_code=204,
)
def delete_restaurant(
    restaurant_id: UUID,
    service: RestaurantService = Depends(get_restaurant_service),
):
    service.delete(restaurant_id)