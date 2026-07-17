from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant


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
        skip: int = 0,
        limit: int = 10,
    ) -> list[Restaurant]:
        stmt = (
            select(Restaurant)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def update(self, restaurant: Restaurant) -> Restaurant:
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete(self, restaurant: Restaurant) -> bool:
        self.db.delete(restaurant)
        self.db.commit()
        return True

