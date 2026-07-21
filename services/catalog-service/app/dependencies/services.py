from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import RestaurantService

def get_restaurant_service(
    db: Session = Depends(get_db),
) -> RestaurantService:
    repository = RestaurantRepository(db)
    return RestaurantService(repository)