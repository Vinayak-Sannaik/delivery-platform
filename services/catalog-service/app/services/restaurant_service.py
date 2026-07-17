from uuid import UUID

from fastapi import HTTPException, status

from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def create(
        self,
        owner_id: UUID,
        restaurant_data: RestaurantCreate,
    ) -> Restaurant:
        existing_restaurant = self.repository.get_by_owner_and_name(
            owner_id=owner_id,
            name=restaurant_data.name,
        )

        if existing_restaurant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant with this name already exists.",
            )

        restaurant = Restaurant(
            owner_id=owner_id,
            **restaurant_data.model_dump(),
        )

        return self.repository.create(restaurant)

    def get_by_id(
        self,
        restaurant_id: UUID,
    ) -> Restaurant:
        restaurant = self.repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )

        return restaurant

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Restaurant]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update(
        self,
        restaurant_id: UUID,
        restaurant_data: RestaurantUpdate,
    ) -> Restaurant:
        restaurant = self.get_by_id(restaurant_id)

        update_data = restaurant_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(restaurant, key, value)

        return self.repository.update(restaurant)

    def delete(
        self,
        restaurant_id: UUID,
    ) -> None:
        restaurant = self.get_by_id(restaurant_id)
        self.repository.delete(restaurant)