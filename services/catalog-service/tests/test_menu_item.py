from uuid import uuid4

from tests.utils import create_access_token


def test_owner_can_create_menu_item(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "Menu Test Restaurant",
            "description": "Testing menu items",
            "phone": "9999999999",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Create category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers=headers,
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create menu item
    menu_item_response = client.post(
        f"/{category_id}/menu_items",
        headers=headers,
        json={
            "name": "Margherita Pizza",
            "price": "299.00",
            "description": "Classic cheese pizza",
            "is_available": True,
        },
    )

    assert menu_item_response.status_code == 201, menu_item_response.text

    data = menu_item_response.json()

    assert data["name"] == "Margherita Pizza"
    assert data["price"] == "299.00"
    assert data["is_available"] is True
    
    
def test_customer_cannot_create_menu_item(client):
    owner_id = str(uuid4())

    owner_token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    owner_headers = {
        "Authorization": f"Bearer {owner_token}",
    }

    # Owner creates restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers=owner_headers,
        json={
            "name": "Customer Menu Test Restaurant",
            "description": "Testing",
            "phone": "8888888888",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Owner creates category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers=owner_headers,
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Customer tries creating menu item
    customer_token = create_access_token(
        user_id=str(uuid4()),
        role="CUSTOMER",
    )

    response = client.post(
        f"/{category_id}/menu_items",
        headers={
            "Authorization": f"Bearer {customer_token}",
        },
        json={
            "name": "Burger",
            "price": "199.00",
            "description": "Unauthorized item",
            "is_available": True,
        },
    )

    assert response.status_code == 403
    
def test_owner_cannot_create_menu_item_for_other_owner_category(client):
    owner_a = str(uuid4())
    owner_b = str(uuid4())

    token_a = create_access_token(
        user_id=owner_a,
        role="RESTAURANT_OWNER",
    )

    token_b = create_access_token(
        user_id=owner_b,
        role="RESTAURANT_OWNER",
    )

    # Owner B creates restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Owner B Restaurant",
            "description": "Testing ownership",
            "phone": "7777777777",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Owner B creates category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Owner A tries creating menu item in Owner B category
    response = client.post(
        f"/{category_id}/menu_items",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
        json={
            "name": "Unauthorized Pizza",
            "price": "299.00",
            "description": "Should fail",
            "is_available": True,
        },
    )

    assert response.status_code == 403
    
def test_owner_can_update_own_menu_item(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "Update Menu Restaurant",
            "description": "Testing",
            "phone": "6666666666",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Create category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers=headers,
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create menu item
    menu_item_response = client.post(
        f"/{category_id}/menu_items",
        headers=headers,
        json={
            "name": "Margherita Pizza",
            "price": "299.00",
            "description": "Original",
            "is_available": True,
        },
    )

    assert menu_item_response.status_code == 201

    menu_item_id = menu_item_response.json()["id"]

    # Update menu item
    update_response = client.put(
        f"/menu-items/{menu_item_id}",
        headers=headers,
        json={
            "name": "Farmhouse Pizza",
            "price": "399.00",
        },
    )

    assert update_response.status_code == 200, update_response.text

    data = update_response.json()

    assert data["name"] == "Farmhouse Pizza"
    assert data["price"] == "399.00"

def test_owner_cannot_update_other_owner_menu_item(client):
    owner_a = str(uuid4())
    owner_b = str(uuid4())

    token_a = create_access_token(
        user_id=owner_a,
        role="RESTAURANT_OWNER",
    )

    token_b = create_access_token(
        user_id=owner_b,
        role="RESTAURANT_OWNER",
    )

    # Owner B creates restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Owner B Menu Restaurant",
            "description": "Testing",
            "phone": "7777777777",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Owner B creates category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Owner B creates menu item
    menu_item_response = client.post(
        f"/{category_id}/menu_items",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Original Pizza",
            "price": "299.00",
            "description": "Owner B item",
            "is_available": True,
        },
    )

    assert menu_item_response.status_code == 201

    menu_item_id = menu_item_response.json()["id"]

    # Owner A tries updating Owner B item
    response = client.put(
        f"/menu-items/{menu_item_id}",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
        json={
            "name": "Hacked Pizza",
        },
    )

    assert response.status_code == 403
    
def test_owner_can_delete_own_menu_item(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "Delete Menu Restaurant",
            "description": "Testing",
            "phone": "5555555555",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Create category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers=headers,
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create menu item
    menu_item_response = client.post(
        f"/{category_id}/menu_items",
        headers=headers,
        json={
            "name": "Delete Pizza",
            "price": "299.00",
            "description": "To delete",
            "is_available": True,
        },
    )

    assert menu_item_response.status_code == 201

    menu_item_id = menu_item_response.json()["id"]

    # Delete menu item
    delete_response = client.delete(
        f"/menu-items/{menu_item_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

def test_owner_cannot_delete_other_owner_menu_item(client):
    owner_a = str(uuid4())
    owner_b = str(uuid4())

    token_a = create_access_token(
        user_id=owner_a,
        role="RESTAURANT_OWNER",
    )

    token_b = create_access_token(
        user_id=owner_b,
        role="RESTAURANT_OWNER",
    )

    # Owner B creates restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Owner B Delete Restaurant",
            "description": "Testing",
            "phone": "4444444444",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Owner B creates category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Owner B creates menu item
    menu_item_response = client.post(
        f"/{category_id}/menu_items",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Owner B Pizza",
            "price": "299.00",
            "description": "Protected item",
            "is_available": True,
        },
    )

    assert menu_item_response.status_code == 201

    menu_item_id = menu_item_response.json()["id"]

    # Owner A tries deleting Owner B item
    response = client.delete(
        f"/menu-items/{menu_item_id}",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
    )

    assert response.status_code == 403


def test_duplicate_menu_item_validation(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant
    restaurant_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "Duplicate Menu Restaurant",
            "description": "Testing",
            "phone": "3333333333",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Create category
    category_response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers=headers,
        json={
            "name": "Pizza",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Create first menu item
    first_response = client.post(
        f"/{category_id}/menu_items",
        headers=headers,
        json={
            "name": "Margherita Pizza",
            "price": "299.00",
            "description": "First item",
            "is_available": True,
        },
    )

    assert first_response.status_code == 201

    # Create duplicate menu item
    duplicate_response = client.post(
        f"/{category_id}/menu_items",
        headers=headers,
        json={
            "name": "Margherita Pizza",
            "price": "399.00",
            "description": "Duplicate item",
            "is_available": True,
        },
    )

    assert duplicate_response.status_code == 409