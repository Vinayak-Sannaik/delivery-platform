from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_by_id(self, category_id: UUID) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        return self.db.scalar(stmt)

    def get_by_restaurant_and_name(
        self,
        restaurant_id: UUID,
        name: str,
    ) -> Category | None:
        stmt = select(Category).where(
            Category.restaurant_id == restaurant_id,
            Category.name == name,
        )
        return self.db.scalar(stmt)

    def list_by_restaurant(
    self,
    restaurant_id: UUID,
    skip: int = 0,
    limit: int = 10,
) -> list[Category]:
        stmt = (
            select(Category)
            .where(Category.restaurant_id == restaurant_id)
            .order_by(Category.created_at)
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> bool:
        self.db.delete(category)
        self.db.commit()
        return True

