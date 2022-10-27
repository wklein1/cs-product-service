from fastapi import FastAPI, status, HTTPException
from deta import Deta, Base
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from models.products_model import (
    ProductsModel,
    ProductsResponseModel,
    ProductsRequestModel,
)
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


@app.get("/products/{user_id}", response_model=list[ProductsResponseModel])
async def get_products_by_user(user_id):
    return productsDB.fetch({"owner_id": user_id}).items


@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductsResponseModel,
    response_description="Returns created product with generated id.",
    description="Create a new product for an user, specified by the ownerId value in request body.",
)
async def post_product_by_user(product: ProductsModel):
    try:
        new_product = product.dict()
        new_product["key"] = str(uuid.uuid1())
        productsDB.insert(new_product)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=ex)
    return new_product