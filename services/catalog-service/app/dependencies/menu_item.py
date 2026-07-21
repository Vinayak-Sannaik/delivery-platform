from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.services.menu_item_service import MenuItemService


def get_menu_item_service(
    db: Session = Depends(get_db),
) -> MenuItemService:
    return MenuItemService(
        category_repo=CategoryRepository(db),
        menu_item_repo=MenuItemRepository(db),
    )