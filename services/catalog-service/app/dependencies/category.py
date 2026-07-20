from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.category_service import CategoryService


def get_category_service(
    db: Session = Depends(get_db),
) -> CategoryService:
    category_repo = CategoryRepository(db)
    restaurant_repo = RestaurantRepository(db)

    return CategoryService(
        category_repo=category_repo,
        restaurant_repo=restaurant_repo,
    )