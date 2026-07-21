from fastapi import HTTPException, status

from app.models.restaurant import Restaurant
from app.models.user import RoleEnum
from app.schemas.auth import CurrentUser


class AuthorizationService:
    def authorize_restaurant_owner(
        self,
        restaurant: Restaurant,
        current_user: CurrentUser,
    ) -> None:
        # Admin can access every restaurant
        if current_user.role == RoleEnum.ADMIN:
            return

        # Owner can access only their own restaurant
        if restaurant.owner_id == current_user.user_id:
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action.",
        )