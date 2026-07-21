from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem


class MenuItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, menu_item: MenuItem) -> MenuItem:
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def get_by_id(self, menu_item_id: UUID) -> MenuItem | None:
        stmt = select(MenuItem).where(MenuItem.id == menu_item_id)
        return self.db.scalar(stmt)

    def get_by_category_and_name(
        self,
        category_id: UUID,
        name: str,
    ) -> MenuItem | None:
        stmt = select(MenuItem).where(
            MenuItem.category_id == category_id,
            MenuItem.name == name,
        )
        return self.db.scalar(stmt)

    def get_all(
        self,
        category_id: UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> list[MenuItem]:
        stmt = (
            select(MenuItem)
            .where(MenuItem.category_id == category_id)
            .order_by(MenuItem.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def update(self, menu_item: MenuItem) -> MenuItem:
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def delete(self, menu_item: MenuItem) -> bool:
        self.db.delete(menu_item)
        self.db.commit()
        return True
    
    def search(
        self,
        category_id: UUID,
        query: str,
        skip: int = 0,
        limit: int = 10,
    ) -> list[MenuItem]:
        
        stmt = (
            select(MenuItem)
            .where(
                MenuItem.category_id == category_id,
                or_(
                    MenuItem.name.ilike(f"%{query}%"),
                    MenuItem.description.ilike(f"%{query}%"),
                ),
            )
            .order_by(MenuItem.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        
        return list(self.db.scalars(stmt).all())
        
    def list_available_by_category(
        self,
        category_id: UUID,
    ) -> list[MenuItem]:
        
        stmt = (
            select(MenuItem)
            .where(
                MenuItem.category_id == category_id,
                MenuItem.is_available.is_(True),
            )
            .order_by(MenuItem.created_at.desc())
        )
        
        return list(self.db.scalars(stmt).all())
