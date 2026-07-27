import asyncio
from uuid import UUID

from app.clients.catalog_client import CatalogClient


async def main():
    client = CatalogClient("localhost:50051")

    items = await client.get_menu_items(
        [
            UUID("11111111-1111-1111-1111-111111111111")
        ]
    )

    print(items)


asyncio.run(main())