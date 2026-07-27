# import asyncio
# from uuid import UUID

# from app.clients.catalog_client import CatalogClient


# async def main():
#     client = CatalogClient("localhost:50051")

#     items = await client.get_menu_items(
#         [
#             UUID("11111111-1111-1111-1111-111111111111")
#         ]
#     )

#     print(f"Items: {items}")


# asyncio.run(main())


import asyncio
from uuid import UUID

from app.clients.catalog_client import CatalogClient


async def main():
    client = CatalogClient("localhost:50051")

    owner_id = await client.get_restaurant_owner(
        UUID("47eefb93-4340-40a0-83c6-bea1bfcb68c5")
    )

    print(f"Owner ID: {owner_id}")

    await client.close()


asyncio.run(main())