import json

from app.services.catalog_client import CatalogClient


class ToolExecutor:

    def __init__(self):
        self.catalog_client = CatalogClient()

    async def execute(
        self,
        tool_name: str,
        arguments,
    ):
        # Groq normally gives tool arguments as a JSON string.
        # Handle both string and already-parsed dict.
        if isinstance(arguments, str):
            args = json.loads(arguments)
        else:
            args = arguments

        if tool_name == "search_menu":
            return await self.catalog_client.search_menu(
                query=args.get("query"),
                min_price=args.get("min_price"),
                max_price=args.get("max_price"),
            )

        if tool_name == "get_menu_item":
            return await self.catalog_client.get_menu_item(
                menu_item_id=args.get("menu_item_id"),
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )