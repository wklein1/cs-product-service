from fastapi import FastAPI
from deta import Deta, Base
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from models.products_model import ProductsModel

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
    expose_headers=["*"])

@app.get("/products/{user_id}",response_model=list[ProductsModel])
async def get_products_by_user(user_id):
    return productsDB.fetch({"owner_id":user_id}).items