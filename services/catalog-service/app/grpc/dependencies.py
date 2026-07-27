from app.core.database import SessionLocal

from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_item_repository import MenuItemRepository

from app.services.authorization_service import AuthorizationService
from app.services.menu_item_service import MenuItemService


def get_menu_item_service() -> MenuItemService:
    db = SessionLocal()

    category_repo = CategoryRepository(db)
    menu_item_repo = MenuItemRepository(db)
    authorization_service = AuthorizationService()

    return MenuItemService(
        category_repo=category_repo,
        menu_item_repo=menu_item_repo,
        authorization_service=authorization_service,
    )