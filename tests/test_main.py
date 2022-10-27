from fastapi.testclient import TestClient
from decouple import config
from main import app

def test_delete_product_endpoint():
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    test_product = {
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from post request",
        "price":0.0
    }
    post_response = client.post("/products",json=test_product)
    product_id = post_response.json()["productId"]
    del_response = client.delete(f"/products/{product_id}",headers={"userId":TEST_USER_ID})
    assert del_response.status_code == 204

def test_get_products_endpoint_returns_products_for_user():
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    response = client.get(f"/products/{TEST_USER_ID}")
    expected_product = {
        "productId":"29f6f518-53a8-11ed-a980-cd9f67f7363d",
        "ownerId":TEST_USER_ID,
        "name":"test product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"",
        "price":0.0
    }
    assert response.status_code == 200
    assert expected_product in response.json()

def test_post_products_endpoint():
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    test_product = {
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from post request",
        "price":0.0
    }
    response = client.post("/products",json=test_product)
    response_product = response.json()
    assert response.status_code == 201
    assert test_product.items() <=response_product.items()
    client.delete(f"/products/{response_product['productId']}",headers={"userId":TEST_USER_ID})

def test_put_endpoint_creates_not_existing_product():
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    test_product = {
        productId:"test_id",
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from post request",
        "price":0.0
    }
    response = client.put("/products",json=test_product)
    response_product = response.json()
    assert response.status_code == 201
    assert test_product == response.json()

