from tests.conftest import client


# def test_health():
#     response = client.get("/health")

#     assert response.status_code == 200
#     assert response.json() == {
#         "status": "ok"
#     }
    
def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200