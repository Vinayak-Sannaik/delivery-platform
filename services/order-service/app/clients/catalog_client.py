from uuid import UUID

import grpc

from app.grpc import catalog_pb2
from app.grpc import catalog_pb2_grpc
from app.core.config import settings

class CatalogClient:

    def __init__(
        self,
    ):
        # print("CATALOG GRPC ADDRESS:", settings.CATALOG_GRPC_ADDRESS)

        self.channel = grpc.aio.insecure_channel(settings.CATALOG_GRPC_ADDRESS)

        self.stub = catalog_pb2_grpc.CatalogServiceStub(
            self.channel
        )

    async def get_menu_items(
        self,
        menu_item_ids: list[UUID],
    ):
        request = catalog_pb2.GetMenuItemsRequest(
            menu_item_ids=[
                str(item_id)
                for item_id in menu_item_ids
            ]
        )

        response = await self.stub.GetMenuItems(request)

        return response.menu_items


    async def get_restaurant_owner(
        self,
        restaurant_id: UUID,
    ):
        request = catalog_pb2.GetRestaurantOwnerRequest(
            restaurant_id=str(restaurant_id)
        )

        response = await self.stub.GetRestaurantOwner(request)

        return response.owner_id


    async def close(self):
        await self.channel.close()