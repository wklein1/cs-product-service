from fastapi import FastAPI, status, HTTPException, Header
from deta import Deta, Base
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from models import product_models,error_models
import uuid

PROJECT_KEY = config("PROJECT_KEY")

deta = Deta(PROJECT_KEY)
productsDB = deta.Base("products")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/products/{user_id}", response_model=list[product_models.ProductResponseModel])
async def get_products_by_user(user_id):
    return productsDB.fetch({"owner_id": user_id}).items


@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=product_models.ProductResponseModel,
    response_description="Returns created product with generated id.",
    description="Create a new product for an user, specified by the ownerId value in request body.",
)
async def post_product_by_user(product: product_models.ProductModel):
    try:
        new_product = product.dict()
        new_product["key"] = str(uuid.uuid1())
        productsDB.insert(new_product)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=ex)
    return new_product


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deletes a product by its id, if the user is the owner.",
)
async def delete_product_by_id(product_id, user_id: str = Header(alias="userId")):
    product_to_delete = productsDB.get(product_id)
    if product_to_delete["owner_id"] == user_id:
        productsDB.delete(product_id)
        return
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.put(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=product_models.ProductResponseModel,
    response_description="Returns created or updated product.",
    responses={403 :{
            "model": error_models.HTTPErrorModel,
            "description": "Error raised if user tries to create or update a product not owned."
        }},
    description="Creates a new product if not existing, else updates product with values in request body.",
)
async def put_product_by_user(product: product_models.ProductRequestModel, user_id: str = Header(alias="userId")):
    product_to_update = productsDB.get(product.dict()["key"])
    if product_to_update and product_to_update["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Modifications are only allowed by the owner of the product.")
    else:
        if(product.dict()["owner_id"]!=user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users are only allowed to create products for themselves.")
        try:
            new_or_updated_product = productsDB.put(product.dict())
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex))
        return new_or_updated_product