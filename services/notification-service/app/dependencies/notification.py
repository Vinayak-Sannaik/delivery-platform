from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.notification_repository import (
    NotificationRepository,
)
from app.services.notification_service import (
    NotificationService,
)


async def get_notification_service(
    db: AsyncSession = Depends(get_db),
) -> NotificationService:

    repository = NotificationRepository(db)

    return NotificationService(
        notification_repository=repository,
    )