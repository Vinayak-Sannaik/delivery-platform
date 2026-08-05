import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from uuid import UUID


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: Order) -> Order:
        """
        Persist a new order.

        Note:
        - Does NOT commit the transaction.
        - Flushes so generated values (e.g. UUID/defaults) are available.
        """
        self.db.add(order)
        await self.db.flush()
        return order

    async def get_by_id(
        self,
        order_id: uuid.UUID,
    ) -> Order | None:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, order: Order) -> None:
        """
        Delete an existing order.

        Note:
        - Does NOT commit the transaction.
        """
        await self.db.delete(order)
        await self.db.flush()
        
    async def update(self, order: Order) -> Order:
        """
        Flush changes to an existing order.
        """
        await self.db.flush()

        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order.id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one()
    
    async def get_by_customer(
        self,
        customer_id: UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Order]:

        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .order_by(Order.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_restaurant(
        self,
        restaurant_id: UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.restaurant_id == restaurant_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
    