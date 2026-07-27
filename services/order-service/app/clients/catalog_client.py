from uuid import UUID

import grpc

from app.grpc.generated import catalog_pb2
from app.grpc.generated import catalog_pb2_grpc


class CatalogClient:
    def __init__(
        self,
        host: str = "localhost:50051",
    ):
        self.channel = grpc.aio.insecure_channel(host)
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

        return response.items

    async def close(self):
        await self.channel.close()