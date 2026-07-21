from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import RoleEnum
from app.schemas.auth import CurrentUser


def require_roles(*allowed_roles: RoleEnum) -> Callable:
    def dependency(
        current_user: CurrentUser = Depends(get_current_user),
    ) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action.",
            )

        return current_user

    return dependency


require_admin = require_roles(RoleEnum.ADMIN)

require_restaurant_owner = require_roles(
    RoleEnum.RESTAURANT_OWNER,
    RoleEnum.ADMIN,
)

require_customer = require_roles(
    RoleEnum.CUSTOMER,
    RoleEnum.ADMIN,
)