from uuid import uuid4

from tests.utils import create_access_token


def test_create_restaurant_as_customer_forbidden(client):
    token = create_access_token(
        user_id=str(uuid4()),
        role="CUSTOMER",
    )

    response = client.post(
        "/restaurants",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Customer Restaurant",
            "description": "Should fail",
            "phone": "9999999999",
            "address": "Pune",
        },
    )

    assert response.status_code == 403

def test_create_restaurant_without_token_unauthorized(client):
    response = client.post(
        "/restaurants",
        json={
            "name": "No Token Restaurant",
            "description": "Should fail",
            "phone": "9999999999",
            "address": "Pune",
        },
    )

    assert response.status_code == 401