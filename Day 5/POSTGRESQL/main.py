from fastapi import FastAPI
from sqlmodel import SQLModel

class Product(SQLModel):
    id: int
    name: str
    price: float
    stock: int
    category_id: int
