# Catalog Service
# │
# ├── PostgreSQL
# │   └── app/core/database.py
# │
# └── Redis
#     └── app/core/redis.py
from upstash_redis import Redis

from app.core.config import settings


redis_client = Redis(
    url=settings.REDIS_URL,
    token=settings.REDIS_TOKEN,
)

RESTAURANT_CACHE_TTL = 300
MENU_ITEM_CACHE_TTL = 300


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


# --------------------------------------------------
# Menu item cache
# --------------------------------------------------

def get_menu_item_cache_key(menu_item_id: str) -> str:
    return f"menu-item:{menu_item_id}"


def get_menu_items_list_cache_key(
    category_id: str,
    name: str | None,
    is_available: bool | None,
    min_price,
    max_price,
    skip: int,
    limit: int,
) -> str:

    name_value = name or "all"

    available_value = (
        str(is_available).lower()
        if is_available is not None
        else "all"
    )

    min_price_value = (
        str(min_price)
        if min_price is not None
        else "all"
    )

    max_price_value = (
        str(max_price)
        if max_price is not None
        else "all"
    )

    return (
        f"menu-items:list:"
        f"{category_id}:"
        f"{name_value}:"
        f"{available_value}:"
        f"{min_price_value}:"
        f"{max_price_value}:"
        f"{skip}:"
        f"{limit}"
    )


def invalidate_menu_items_cache(
    category_id: str,
) -> None:

    pattern = (
        f"menu-items:list:{category_id}:*"
    )

    for key in redis_client.scan_iter(
        match=pattern
    ):
        redis_client.delete(key)