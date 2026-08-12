import json
from uuid import UUID

from fastapi import HTTPException, status, Request

from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.authorization_service import AuthorizationService
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.repositories.idempotency_repository import IdempotencyRepository
from app.schemas.auth import CurrentUser

from app.core.redis import redis_client, get_restaurant_cache_key, RESTAURANT_CACHE_TTL


class RestaurantService:
    def __init__(
        self,
        repository: RestaurantRepository,
        authorization_service: AuthorizationService,
        idempotency_repository: IdempotencyRepository
    ):
        self.repository = repository
        self.authorization_service = authorization_service
        self.idempotency_repository = idempotency_repository

    # def _authorize_restaurant_owner(
    #     self,
    #     restaurant: Restaurant,
    #     current_user: CurrentUser,
    # ) -> None:
    #     # Admin can manage every restaurant
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
        owner_id: UUID,
        restaurant_data: RestaurantCreate,
        request: Request
    ) -> Restaurant:
        
        idempotency_key = request.headers.get("idempotency-key")
        
        if idempotency_key:
            existing_key = self.idempotency_repository.get_by_key(
                idempotency_key
            )
            
            if existing_key:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Duplicate idempotency key.",
                )
            
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
    ) -> RestaurantResponse:

        cache_key = get_restaurant_cache_key(
            str(restaurant_id)
        )

        # -----------------------------
        # 1. Redis cache lookup
        # -----------------------------
        cached = redis_client.get(cache_key)

        if cached:
            print("FROM CACHE")
            return RestaurantResponse.model_validate_json(
                cached
            )

        # -----------------------------
        # 2. PostgreSQL fallback
        # -----------------------------
        restaurant = self.repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )

        response = RestaurantResponse.model_validate(
            restaurant,
            from_attributes=True,
        )
        
        print("FROM DB")

        # -----------------------------
        # 3. Store in Redis
        # -----------------------------
        redis_client.setex(
            cache_key,
            RESTAURANT_CACHE_TTL,
            response.model_dump_json(),
        )

        return response

    def get_all(
        self,
        name: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Restaurant]:
        return self.repository.get_all(name = name, is_active = is_active, skip=skip, limit=limit)

    def update(
        self,
        restaurant_id: UUID,
        restaurant_data: RestaurantUpdate,
        current_user: CurrentUser,
    ) -> Restaurant:

        restaurant = self.get_by_id_from_database(
            restaurant_id
        )

        self.authorization_service.authorize_restaurant_owner(
            restaurant,
            current_user,
        )

        update_data = restaurant_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(restaurant, key, value)

        updated_restaurant = self.repository.update(
            restaurant
        )

        # Invalidate stale cache
        cache_key = get_restaurant_cache_key(
            str(restaurant_id)
        )

        redis_client.delete(cache_key)

        return updated_restaurant

    def delete(
        self,
        restaurant_id: UUID,
        current_user: CurrentUser,
    ) -> None:

        restaurant = self.get_by_id_from_database(
            restaurant_id
        )

        self.authorization_service.authorize_restaurant_owner(
            restaurant,
            current_user,
        )

        self.repository.delete(restaurant)

        # Remove stale cache
        cache_key = get_restaurant_cache_key(
            str(restaurant_id)
        )

        redis_client.delete(cache_key)

    def get_by_id_from_database(
        self,
        restaurant_id: UUID,
    ) -> Restaurant:

        restaurant = self.repository.get_by_id(
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )

        return restaurant