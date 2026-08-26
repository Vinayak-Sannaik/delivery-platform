MENU_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_menu",
        "description": (
            "Search available menu items. "
            "Use this when the user wants to find food, "
            "menu items, or food within a price range."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The food or menu item the user is looking for."
                    ),
                },
                "min_price": {
                    "type": "number",
                    "description": (
                        "Minimum price."
                    ),
                },
                "max_price": {
                    "type": "number",
                    "description": (
                        "Maximum price."
                    ),
                },
            },
            "required": [],
        },
    },
}