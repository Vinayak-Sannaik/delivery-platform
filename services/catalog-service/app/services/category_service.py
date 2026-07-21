from uuid import UUID

from fastapi import HTTPException, status

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.category import CategoryCreate, CategoryUpdate

from app.schemas.auth import CurrentUser
from app.models.user import RoleEnum
from app.models.restaurant import Restaurant
from app.services.authorization_service import AuthorizationService



class CategoryService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        restaurant_repo: RestaurantRepository,
        authorization_service: AuthorizationService
    ):
        self.category_repo = category_repo
        self.restaurant_repo = restaurant_repo
        self.authorization_service = authorization_service
        
    # def authorization_service(
    #     self,
    #     restaurant: Restaurant,
    #     current_user: CurrentUser,
    # ) -> None:
    #     # Admin can manage every restaurant and category
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
        restaurant_id: UUID,
        category_data: CategoryCreate,
        current_user: CurrentUser
    ) -> Category:
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        
        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )

        self.authorization_service.authorize_restaurant_owner(
            restaurant,
            current_user,
        )

        existing_category = self.category_repo.get_by_restaurant_and_name(
            restaurant_id=restaurant_id,
            name=category_data.name,
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

        category = Category(
            restaurant_id=restaurant_id,
            name=category_data.name,
        )

        return self.category_repo.create(category)

    def get_by_id(
        self,
        category_id: UUID,
    ) -> Category:
        category = self.category_repo.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category

    def list_by_restaurant(
        self,
        restaurant_id: UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Category]:
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )

        return self.category_repo.list_by_restaurant(
            restaurant_id=restaurant_id,
            skip=skip,
            limit=limit,
        )

    def update(
        self,
        category_id: UUID,
        category_data: CategoryUpdate,
        current_user: CurrentUser
    ) -> Category:
        category = self.get_by_id(category_id)

        self.authorization_service.authorize_restaurant_owner(
            category.restaurant,
            current_user,
        )
        
        if (
            category_data.name
            and category_data.name != category.name
        ):
            existing_category = (
                self.category_repo.get_by_restaurant_and_name(
                    restaurant_id=category.restaurant_id,
                    name=category_data.name,
                )
            )

            if existing_category:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category already exists.",
                )

        update_data = category_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(category, key, value)
            
        

        return self.category_repo.update(category)

    def delete(
        self,
        category_id: UUID,
        current_user: CurrentUser
    ) -> None:
        
        category = self.get_by_id(category_id)
        
        self.authorization_service.authorize_restaurant_owner(
                category.restaurant,
                current_user,
         )
        self.category_repo.delete(category)