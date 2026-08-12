# Catalog Service
# │
# ├── PostgreSQL
# │   └── app/core/database.py
# │
# └── Redis
#     └── app/core/redis.py
import redis

from app.core.config import settings


redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


RESTAURANT_CACHE_TTL = 300


def get_restaurant_cache_key(restaurant_id: str) -> str:
    return f"restaurant:{restaurant_id}"