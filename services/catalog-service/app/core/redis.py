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


def get_restaurants_list_cache_key(
    name: str | None,
    is_active: bool | None,
    skip: int,
    limit: int,
) -> str:
    name_value = name or "all"
    active_value = (
        str(is_active).lower()
        if is_active is not None
        else "all"
    )

    return (
        f"restaurants:list:"
        f"{name_value}:"
        f"{active_value}:"
        f"{skip}:"
        f"{limit}"
    )
    
    
def invalidate_restaurant_list_cache() -> None:
    keys = redis_client.scan_iter(
        match="restaurants:list:*"
    )

    for key in keys:
        redis_client.delete(key)