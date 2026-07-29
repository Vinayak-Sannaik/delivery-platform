import logging

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

RETRY_STATUS_CODES = {502, 503, 504}


def should_retry(exception: Exception) -> bool:
    if isinstance(exception, (httpx.ConnectError, httpx.ReadTimeout)):
        return True

    if isinstance(exception, httpx.HTTPStatusError):
        return exception.response.status_code in RETRY_STATUS_CODES

    return False


class CatalogHttpClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.CATALOG_SERVICE_URL,
            timeout=httpx.Timeout(10.0),
        )

    async def close(self):
        await self.client.aclose()

    @retry(
        retry=retry_if_exception(should_retry),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def get_menu_items(
        self,
        menu_item_ids: list[str],
    ):
        response = await self.client.post(
            "/internal/menu-items",
            json={
                "menu_item_ids": [
                    str(item_id)
                    for item_id in menu_item_ids
                ]
            },
        )

        response.raise_for_status()

        return [
            type(
                "MenuItemDTO",
                (),
                {
                    "id": item["id"],
                    "restaurant_id": item["restaurant_id"],
                    "name": item["name"],
                    "price": item["price"],
                    "is_available": item["is_available"],
                },
            )
            for item in response.json()
        ]

    @retry(
        retry=retry_if_exception(should_retry),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def get_restaurant_owner(
        self,
        restaurant_id: str,
    ):
        response = await self.client.get(
            f"/internal/restaurants/{restaurant_id}/owner"
        )

        response.raise_for_status()

        return response.json()