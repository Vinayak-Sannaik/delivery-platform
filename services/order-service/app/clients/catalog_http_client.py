import httpx

from app.core.config import settings


class CatalogHttpClient:

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.CATALOG_SERVICE_URL
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


    async def get_restaurant_owner(
        self,
        restaurant_id: str,
    ):
        response = await self.client.get(
            f"/internal/restaurants/{restaurant_id}/owner"
        )

        response.raise_for_status()

        return response.json()