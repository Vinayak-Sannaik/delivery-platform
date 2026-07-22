import os

import pytest
from fastapi.testclient import TestClient
from app.core.database import Base, engine

os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@localhost:5433/catalog_test_db"
os.environ["JWT_SECRET_KEY"] = "_SD_j0QDubom_9Doj9QBP4CUHNwzq8_jW4t2pqKOGXQ"
os.environ["JWT_ALGORITHM"] = "HS256"

from app.main import app


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client