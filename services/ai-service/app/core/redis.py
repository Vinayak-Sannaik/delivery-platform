from upstash_redis import Redis

from app.core.config import settings


redis_client = Redis(
    url=settings.REDIS_URL,
    token=settings.REDIS_TOKEN,
)

RESTAURANT_CACHE_TTL = 300
MENU_ITEM_CACHE_TTL = 300