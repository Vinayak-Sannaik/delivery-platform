from uuid import UUID

from fastapi import HTTPException, status

from app.models.menu_item import MenuItem
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.schemas.menu_item import CreateMenuItem, UpdateMenuItem


class MenuItemService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        menu_item_repo: MenuItemRepository,
    ):
        self.category_repo = category_repo
        self.menu_item_repo = menu_item_repo

    def create(
        self,
        category_id: UUID,
        menu_item_data: CreateMenuItem,
    ) -> MenuItem:

        category = self.category_repo.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        existing_menu_item = self.menu_item_repo.get_by_category_and_name(
            category_id=category_id,
            name=menu_item_data.name,
        )

        if existing_menu_item:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Menu item already exists.",
            )

        menu_item = MenuItem(
            category_id=category_id,
            name=menu_item_data.name,
            description=menu_item_data.description,
            price=menu_item_data.price,
            is_available=menu_item_data.is_available,
        )

        return self.menu_item_repo.create(menu_item)

    def get_by_id(
        self,
        menu_item_id: UUID,
    ) -> MenuItem:

        menu_item = self.menu_item_repo.get_by_id(menu_item_id)

        if menu_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found.",
            )

        return menu_item

    def list_by_category(
        self,
        category_id: UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> list[MenuItem]:

        category = self.category_repo.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return self.menu_item_repo.get_all(
            category_id=category_id,
            skip=skip,
            limit=limit,
        )

    def update(
        self,
        menu_item_id: UUID,
        menu_item_data: UpdateMenuItem,
    ) -> MenuItem:

        menu_item = self.get_by_id(menu_item_id)

        if (
            menu_item_data.name
            and menu_item_data.name != menu_item.name
        ):
            existing_menu_item = (
                self.menu_item_repo.get_by_category_and_name(
                    category_id=menu_item.category_id,
                    name=menu_item_data.name,
                )
            )

            if existing_menu_item:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Menu item already exists.",
                )

        update_data = menu_item_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(menu_item, key, value)

        return self.menu_item_repo.update(menu_item)

    def delete(
        self,
        menu_item_id: UUID,
    ) -> None:

        menu_item = self.get_by_id(menu_item_id)
        self.menu_item_repo.delete(menu_item)