from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_item import OrderItem


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(
        self,
        order_items: list[OrderItem],
    ) -> None:
        self.db.add_all(order_items)
        await self.db.flush()