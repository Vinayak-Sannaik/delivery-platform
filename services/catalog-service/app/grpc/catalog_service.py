from uuid import UUID

from app.grpc.dependencies import get_menu_item_service
from app.grpc.generated import catalog_pb2
from app.grpc.generated import catalog_pb2_grpc


class CatalogServiceServicer(catalog_pb2_grpc.CatalogServiceServicer):

    def __init__(self):
        self.menu_item_service = get_menu_item_service()

    async def GetMenuItems(self, request, context):

        menu_item_ids = [
            UUID(item_id)
            for item_id in request.menu_item_ids
        ]

        menu_items = self.menu_item_service.get_menu_items_by_ids(
            menu_item_ids
        )

        return catalog_pb2.GetMenuItemsResponse(
            items=[
                catalog_pb2.MenuItem(
                    id=str(item.id),
                    name=item.name,
                    price=float(item.price),
                    is_available=item.is_available,
                )
                for item in menu_items
            ]
        )