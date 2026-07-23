from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import RestaurantService
from app.services.authorization_service import AuthorizationService
from app.repositories.idempotency_repository import IdempotencyRepository

def get_restaurant_service(
    db: Session = Depends(get_db),
) -> RestaurantService:
    return RestaurantService(
        repository=RestaurantRepository(db),
        authorization_service = AuthorizationService(),
        idempotency_repository=IdempotencyRepository(db),
    )