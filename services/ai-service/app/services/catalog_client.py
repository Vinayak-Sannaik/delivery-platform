import httpx

from app.core.config import settings


class CatalogClient:

    async def search_menu(
        self,
        query: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ):
        params = {
            "name": query,
            "min_price": min_price,
            "max_price": max_price,
            "is_available": True,
            "skip": 0,
            "limit": 20,
        }

        # Remove None values
        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        url = (
            f"{settings.catalog_service_url}"
            "/menu-items/search"
        )

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                url,
                params=params,
            )

            response.raise_for_status()

            return response.json()