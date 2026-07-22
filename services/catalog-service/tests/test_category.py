from uuid import uuid4

from tests.utils import create_access_token


def test_owner_can_create_category(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant first
    restaurant_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "Category Test Restaurant",
            "description": "Testing categories",
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

    data = category_response.json()

    assert data["name"] == "Pizza"
    assert data["restaurant_id"] == restaurant_id
    
    


def test_customer_cannot_create_category(client):
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
            "name": "Customer Category Test Restaurant",
            "description": "Testing",
            "phone": "8888888888",
            "address": "Pune",
        },
    )

    assert restaurant_response.status_code == 201

    restaurant_id = restaurant_response.json()["id"]

    # Customer tries creating category
    customer_token = create_access_token(
        user_id=str(uuid4()),
        role="CUSTOMER",
    )

    response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers={
            "Authorization": f"Bearer {customer_token}",
        },
        json={
            "name": "Burger",
        },
    )

    assert response.status_code == 403
    
    
def test_owner_cannot_create_category_for_other_owner_restaurant(client):
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

    # Owner A tries creating category
    response = client.post(
        f"/restaurants/{restaurant_id}/categories",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
        json={
            "name": "Unauthorized Category",
        },
    )

    assert response.status_code == 403
    
def test_owner_can_update_own_category(client):
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
            "name": "Category Update Restaurant",
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
            "name": "Old Category",
        },
    )

    assert category_response.status_code == 201

    category_id = category_response.json()["id"]

    # Update category
    update_response = client.put(
        f"/categories/{category_id}",
        headers=headers,
        json={
            "name": "Updated Category",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["name"] == "Updated Category"