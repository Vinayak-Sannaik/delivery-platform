from uuid import UUID

from fastapi import HTTPException, status

from app.models.notification import Notification
from app.repositories.notification_repository import (
    NotificationRepository,
)


class NotificationService:
    def __init__(
        self,
        notification_repository: NotificationRepository,
    ):
        self.notification_repository = notification_repository

    async def create_notification(
        self,
        user_id: UUID,
        title: str,
        message: str,
        type: str,
    ) -> Notification:

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
        )

        return await self.notification_repository.create(
            notification
        )

    async def get_notifications(
        self,
        user_id: UUID,
    ):
        return await self.notification_repository.get_by_user(
            user_id
        )

    async def mark_read(
        self,
        notification_id: UUID,
        user_id: UUID,
    ):
        notification = (
            await self.notification_repository.get_by_id(
                notification_id
            )
        )

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
            
        if notification.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized",
            )

        notification.is_read = True

        return await self.notification_repository.update(
            notification
        )

    async def mark_all_read(
        self,
        user_id: UUID,
    ):
        notifications = (
            await self.notification_repository.get_by_user(
                user_id
            )
        )
        
        
        for notification in notifications:
            notification.is_read = True

        await self.notification_repository.db.flush()

        return notifications