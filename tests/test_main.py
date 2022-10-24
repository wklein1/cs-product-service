from fastapi.testclient import TestClient
from decouple import config
from main import app

def test_get_product_endpoint_returns_products_for_user():
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    response = client.get(f"/products/{TEST_USER_ID}")
    assert response.status_code == 200
    assert response.json()[0] == {
    "productId":"29f6f518-53a8-11ed-a980-cd9f67f7363d",
    "ownerId":TEST_USER_ID,
    "name":"test product",
    "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
    "description":"",
    "price":0.0
}