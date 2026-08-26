import json

from app.services.catalog_client import CatalogClient


class ToolExecutor:

    def __init__(self):
        self.catalog_client = CatalogClient()

    async def execute(
        self,
        tool_name: str,
        arguments: str,
    ):
        if tool_name == "search_menu":
            args = json.loads(arguments)

            return await self.catalog_client.search_menu(
                query=args.get("query"),
                min_price=args.get("min_price"),
                max_price=args.get("max_price"),
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )