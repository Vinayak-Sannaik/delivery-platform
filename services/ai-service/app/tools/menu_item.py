GET_MENU_ITEM_TOOL = {
    "type": "function",
    "function": {
        "name": "get_menu_item",
        "description": (
            "Get detailed information about a specific menu item. "
            "Use this when the user asks for details about a menu item."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "menu_item_id": {
                    "type": "string",
                    "description": "The UUID of the menu item.",
                }
            },
            "required": ["menu_item_id"],
        },
    },
}