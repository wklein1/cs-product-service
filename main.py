from fastapi import FastAPI
from deta import Deta, Base
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

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