from uuid import uuid4

from tests.utils import create_access_token


def test_create_duplicate_restaurant_name(client):
    user_id = str(uuid4())

    token = create_access_token(
        user_id=user_id,
        role="RESTAURANT_OWNER",
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "name": "Burger House",
        "description": "First restaurant",
        "phone": "9999999999",
        "address": "Pune",
    }

    first_response = client.post(
        "/restaurants",
        headers=headers,
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/restaurants",
        headers=headers,
        json=payload,
    )

    assert second_response.status_code == 400