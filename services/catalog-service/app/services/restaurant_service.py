from uuid import UUID

from fastapi import HTTPException, status

from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.schemas.auth import CurrentUser
from app.models.user import RoleEnum

class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository
        
    def _authorize_restaurant_owner(
        self,
        restaurant: Restaurant,
        current_user: CurrentUser,
    ) -> None:
        # Admin can manage every restaurant
        if current_user.role == RoleEnum.ADMIN:
            return

        # Restaurant owner can manage only their own restaurant
        if restaurant.owner_id == current_user.user_id:
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action on this restaurant.",
        )
        
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
        current_user: CurrentUser,
    ) -> Restaurant:
        restaurant = self.get_by_id(restaurant_id)
        
        self._authorize_restaurant_owner(
            restaurant,
            current_user,
        )

        update_data = restaurant_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(restaurant, key, value)

        return self.repository.update(restaurant)

    def delete(
        self,
        restaurant_id: UUID,
        current_user: CurrentUser,
    ) -> None:
        restaurant = self.get_by_id(restaurant_id)

        self._authorize_restaurant_owner(
            restaurant,
            current_user,
        )

        self.repository.delete(restaurant)