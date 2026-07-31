from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.notification import (
    get_notification_service,
)
from app.schemas.auth import CurrentUser
from app.schemas.notification import NotificationResponse
from app.services.notification_service import (
    NotificationService,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "/me",
    response_model=list[NotificationResponse],
)
async def get_my_notifications(
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: NotificationService = Depends(
        get_notification_service,
    ),
):
    return await service.get_notifications(
        current_user.user_id,
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
async def mark_notification_read(
    notification_id: UUID,
    service: NotificationService = Depends(
        get_notification_service,
    ),
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
):
    return await service.mark_read(
        notification_id,
        current_user.user_id,
    )


@router.patch(
    "/read-all",
    response_model=list[NotificationResponse],
)
async def mark_all_notifications_read(
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: NotificationService = Depends(
        get_notification_service,
    ),
):
    return await service.mark_all_read(
        current_user.user_id,
    )