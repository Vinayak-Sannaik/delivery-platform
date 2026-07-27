import os
from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient, ASGITransport


import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(BASE_DIR)
)

from app.db.base import Base

from app.core.database import (
    engine,
    AsyncSessionLocal,
)

from app.main import app


os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://postgres:postgres@localhost:5433/order_test_db"
)

os.environ["JWT_SECRET_KEY"] = (
    "_BD_j0QDubom_9Doj9QBP4CUHNwzq8_jW4t2pqKOGXQ"
)

os.environ["JWT_ALGORITHM"] = "HS256"


@pytest_asyncio.fixture(autouse=True)
async def clean_database():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def db_session():

    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
        
        
        

class FakeMenuItem:
    def __init__(
        self,
        id,
        restaurant_id,
        name,
        price,
        is_available,
    ):
        self.id = str(id)
        self.restaurant_id = str(restaurant_id)
        self.name = name
        self.price = str(price)
        self.is_available = is_available


class FakeCatalogClient:

    async def get_menu_items(
        self,
        menu_item_ids,
    ):
        restaurant_id = uuid4()

        return [
            FakeMenuItem(
                id=item_id,
                restaurant_id=restaurant_id,
                name="Burger",
                price="100.00",
                is_available=True,
            )
            for item_id in menu_item_ids
        ]

    async def get_restaurant_owner(
        self,
        restaurant_id,
    ):
        return uuid4()