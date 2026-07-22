from uuid import uuid4

from tests.utils import create_access_token


def test_create_restaurant_success(client):
    token = create_access_token(
        user_id=str(uuid4()),
        role="RESTAURANT_OWNER",
    )

    response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Pizza Palace",
            "description": "Best pizza in town",
            "phone": "9876543210",
            "address": "Pune",
            "image_url": "https://example.com/pizza.jpg",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Pizza Palace"
    assert data["description"] == "Best pizza in town"
    assert data["phone"] == "9876543210"
    assert data["address"] == "Pune"
    assert data["owner_id"] is not None