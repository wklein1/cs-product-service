from fastapi.testclient import TestClient
from decouple import config
from main import app
import uuid

def test_delete_product_endpoint():
    #ARRANGE
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
    #ACT
    del_response = client.delete(f"/products/{product_id}",headers={"userId":TEST_USER_ID})
    #ASSERT
    assert del_response.status_code == 204


def test_get_products_endpoint_returns_products_for_user():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    expected_product = {
        "productId":"29f6f518-53a8-11ed-a980-cd9f67f7363d",
        "ownerId":TEST_USER_ID,
        "name":"test product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"test product for get method",
        "price":0.0
    }
    #ACT
    response = client.get(f"/products/{TEST_USER_ID}")
    #ASSERT
    assert response.status_code == 200
    assert expected_product in response.json()


def test_get_single_product_endpoint_returns_product_for_user_by_id():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    expected_product = {
        "productId":"29f6f518-53a8-11ed-a980-cd9f67f7363d",
        "ownerId":TEST_USER_ID,
        "name":"test product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"test product for get method",
        "price":0.0
    }
    expected_product_id = expected_product['productId']
    #ACT
    response = client.get(f"/products/{expected_product_id}", headers={"userId":TEST_USER_ID})
    #ASSERT
    assert response.status_code == 200
    assert response.json() == expected_product


def test_get_single_product_endpoint_fails_for_not_existing_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    expected_error = {
        "detail": "Product not found."
    }
    #ACT
    response = client.get("/products/not_existing_id", headers={"userId":TEST_USER_ID})
    #ASSERT
    assert response.status_code == 404
    assert response.json() == expected_error


def test_get_single_product_endpoint_fails_for_not_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    expected_product = {
        "productId":"29f6f518-53a8-11ed-a980-cd9f67f7363d",
        "ownerId":TEST_USER_ID,
        "name":"test product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"",
        "price":0.0
    }
    expected_error = {
        "detail": "User is not allowed to get a product not owned."
    }
    expected_product_id = expected_product['productId']
    #ACT
    response = client.get(f"/products/{expected_product_id}", headers={"userId":"different user id"})
    #ASSERT
    assert response.status_code == 403
    assert response.json() == expected_error


def test_post_products_endpoint():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    test_product = {
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from post request",
        "price":0.0
    }
    #ACT
    response = client.post("/products",json=test_product)
    #ASSERT
    response_product = response.json()
    assert response.status_code == 201
    assert test_product.items() <=response_product.items()
    #CLEANUP
    client.delete(f"/products/{response_product['productId']}",headers={"userId":TEST_USER_ID})


def test_put_endpoint_creates_not_existing_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from put request",
        "price":0.0
    }
    #ACT
    response = client.put("/products",json=test_product, headers={"userId":TEST_USER_ID})
    #ASSERT
    response_product = response.json()
    assert response.status_code == 201
    assert test_product == response.json()
    #CLEANUP
    client.delete(f"/products/{response_product['productId']}",headers={"userId":TEST_USER_ID})


def test_put_endpoint_fails_creating_not_existing_not_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    test_product = {
        "productId":random_test_id,
        "ownerId":"different user id",
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from put request",
        "price":0.0
    }
    expected_error = {
        "detail": "Users are only allowed to create products for themselves."
    }
    #ACT
    response = client.put("/products",json=test_product, headers={"userId":TEST_USER_ID})
    #ASSERT
    assert response.status_code == 403
    assert response.json() == expected_error


def test_put_endpoint_updates_existing_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from post request",
        "price":0.0
    }
    updated_test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test updated product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"updated product from put request",
        "price":0.0
    }
    put_create_response = client.put("/products",json=test_product, headers={"userId":TEST_USER_ID})
    response_product_id = put_create_response.json()["productId"]
    assert put_create_response.status_code == 201
    #ACT
    put_update_response = client.put("/products",json=updated_test_product, headers={"userId":TEST_USER_ID})
    #ASSERT
    assert put_update_response.status_code == 201
    assert updated_test_product == put_update_response.json()
    #CLEANUP
    client.delete(f"/products/{response_product_id}",headers={"userId":TEST_USER_ID})


def test_put_endpoint_fails_updating_existing_not_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from post request",
        "price":0.0
    }
    updated_test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test updated product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"updated product from put request",
        "price":0.0
    }
    expected_error = {
        "detail": "Modifications are only allowed by the owner of the product."
    }
    put_create_response = client.put("/products",json=test_product, headers={"userId":TEST_USER_ID})
    response_product_id = put_create_response.json()["productId"]
    assert put_create_response.status_code == 201
    #ACT
    put_update_response = client.put("/products",json=updated_test_product, headers={"userId":"different user id"})
    #ASSERT
    assert put_update_response.status_code == 403
    assert put_update_response.json() == expected_error
    #CLEANUP
    client.delete(f"/products/{response_product_id}",headers={"userId":TEST_USER_ID})


def test_patch_endpoint_updates_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from put request",
        "price":0.0
    }
    updated_test_product = {
        "ownerId":TEST_USER_ID,
        "name":"test patched product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"updated product from patch request",
        "price":0.0
    }
    put_create_response = client.put("/products",json=test_product, headers={"userId":TEST_USER_ID})
    response_product_id = put_create_response.json()["productId"]
    assert put_create_response.status_code == 201
    #ACT
    patch_response = client.patch(f"/products/{random_test_id}",json=updated_test_product, headers={"userId":TEST_USER_ID})
    #ASSERT
    assert patch_response.status_code == 204
    #CLEANUP
    client.delete(f"/products/{response_product_id}",headers={"userId":TEST_USER_ID})

    
def test_patch_endpoint_fails_updating_not_owned_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    test_product = {
        "productId":random_test_id,
        "ownerId":TEST_USER_ID,
        "name":"test new product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"new product from put request",
        "price":0.0
    }
    updated_test_product = {
        "ownerId":TEST_USER_ID,
        "name":"test patched product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"updated product from patch request",
        "price":0.0
    }
    expected_error = {
        "detail": "Modifications are only allowed by the owner of the product."
    }
    put_create_response = client.put("/products",json=test_product, headers={"userId":TEST_USER_ID})
    response_product_id = put_create_response.json()["productId"]
    assert put_create_response.status_code == 201
    #ACT
    patch_response = client.patch(f"/products/{random_test_id}",json=updated_test_product, headers={"userId":"different user id"})
    #ASSERT
    assert patch_response.status_code == 403
    assert patch_response.json() == expected_error


def test_patch_endpoint_fails_updating_not_existing_product():
    #ARRANGE
    client = TestClient(app)
    TEST_USER_ID = config("TEST_USER_ID")
    random_test_id = str(uuid.uuid1())
    updated_test_product = {
        "ownerId":TEST_USER_ID,
        "name":"test patched product",
        "componentIds":["546c08d7-539d-11ed-a980-cd9f67f7363d","546c08da-539d-11ed-a980-cd9f67f7363d"],
        "description":"updated product from patch request",
        "price":0.0
    }
    expected_error = {
        "detail": "Product not found."
    }
    #ACT
    patch_response = client.patch(f"/products/{random_test_id}",json=updated_test_product, headers={"userId":"different user id"})
    #ASSERT
    # assert patch_response.status_code == 404
    assert patch_response.json() == expected_error
    
    