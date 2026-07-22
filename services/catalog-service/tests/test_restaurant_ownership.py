from uuid import uuid4

from tests.utils import create_access_token


def test_owner_cannot_update_other_owner_restaurant(client):
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
    create_response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Owner B Restaurant",
            "description": "Original",
            "phone": "9999999999",
            "address": "Pune",
        },
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    # Owner A tries updating Owner B restaurant
    update_response = client.put(
        f"/restaurants/{restaurant_id}",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
        json={
            "description": "Hacked update",
        },
    )

    assert update_response.status_code == 403
    

def test_owner_cannot_delete_other_owner_restaurant(client):
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
    create_response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
        json={
            "name": "Owner B Delete Test",
            "description": "Original",
            "phone": "8888888888",
            "address": "Pune",
        },
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    # Owner A tries deleting Owner B restaurant
    delete_response = client.delete(
        f"/restaurants/{restaurant_id}",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
    )

    assert delete_response.status_code == 403
    
def test_owner_can_update_own_restaurant(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant
    create_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "My Restaurant",
            "description": "Old description",
            "phone": "9999999999",
            "address": "Pune",
        },
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    # Update own restaurant
    update_response = client.put(
        f"/restaurants/{restaurant_id}",
        headers=headers,
        json={
            "name": "Updated Restaurant",
            "description": "New description",
            "is_active": True,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["name"] == "Updated Restaurant"
    assert data["description"] == "New description"
    assert data["is_active"] is True
    
    
def test_owner_can_delete_own_restaurant(client):
    owner_id = str(uuid4())

    token = create_access_token(
        user_id=owner_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Create restaurant
    create_response = client.post(
        "/restaurants",
        headers=headers,
        json={
            "name": "Delete My Restaurant",
            "description": "Temporary",
            "phone": "7777777777",
            "address": "Pune",
        },
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    # Delete restaurant
    delete_response = client.delete(
        f"/restaurants/{restaurant_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    # Verify deleted
    get_response = client.get(
        f"/restaurants/{restaurant_id}",
    )

    assert get_response.status_code == 404