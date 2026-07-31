from uuid import UUID

from sqlalchemy import select

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db):
        self.db = db

    async def create(
        self,
        notification: Notification,
    ) -> Notification:
        self.db.add(notification)
        await self.db.flush()
        await self.db.refresh(notification)

        return notification

    async def get_by_user(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        return result.scalars().all()

    async def get_by_id(
        self,
        notification_id: UUID,
    ):
        result = await self.db.execute(
            select(Notification)
            .where(Notification.id == notification_id)
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        notification: Notification,
    ) -> Notification:
        await self.db.flush()
        await self.db.refresh(notification)

        return notification