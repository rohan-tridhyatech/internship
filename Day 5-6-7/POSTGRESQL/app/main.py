from fastapi import FastAPI
from app import lifespan
from app import category, product, orders

app = FastAPI(lifespan=lifespan, title="Product Management App")

app.include_router(category.router, prefix="/category", tags=["Category"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
