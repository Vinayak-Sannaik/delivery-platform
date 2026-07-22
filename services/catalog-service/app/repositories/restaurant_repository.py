from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.category import Category


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, restaurant: Restaurant) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def get_by_id(self, restaurant_id: UUID) -> Restaurant | None:
        stmt = select(Restaurant).where(Restaurant.id == restaurant_id)
        return self.db.scalar(stmt)

    def get_by_owner_and_name(
        self,
        owner_id: UUID,
        name: str,
    ) -> Restaurant | None:
        stmt = select(Restaurant).where(
            Restaurant.owner_id == owner_id,
            Restaurant.name == name,
        )
        return self.db.scalar(stmt)

    def get_all(
        self,
        name: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Restaurant]:
        
        stmt = (select(Restaurant))
        
        if name:
            stmt = stmt.where(Restaurant.name.ilike(f"%{name}%"))
        if is_active is not None:
            stmt = stmt.where(Restaurant.is_active == is_active)
    
        stmt = stmt.offset(skip).limit(limit)
            
        return list(self.db.scalars(stmt).all())

    def update(self, restaurant: Restaurant) -> Restaurant:
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete(self, restaurant: Restaurant) -> bool:
        self.db.delete(restaurant)
        self.db.commit()
        return True
    
    def search(
        self,
        restaurant_id: UUID,
        query: str,
        skip: int = 0,
        limit: int = 10,
    ) -> list[MenuItem]:
        
        stmt = (
            select(MenuItem).join(Category)
            .where(
                MenuItem.restaurant_id == restaurant_id,
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

