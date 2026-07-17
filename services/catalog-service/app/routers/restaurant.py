from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services.restaurant_service import RestaurantService

from app.dependencies.services import get_restaurant_service

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
):
    # TODO: Replace with authenticated user's ID from Gateway
    owner_id = UUID("11111111-1111-1111-1111-111111111111")

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