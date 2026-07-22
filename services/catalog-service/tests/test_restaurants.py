def test_get_restaurants_empty(client):
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert response.json() == []