from __future__ import annotations

from app.auth import admin_only
from app.database import get_session
from app.models import Product
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel import Session

# Importing models, database session, and authentication utilities

router = APIRouter()

# Endpoint to create a new product (POST /)


@router.post("/", response_model=Product, dependencies=[Depends(admin_only)])
async def create_product(product: Product, session: Session = Depends(get_session)):
    # Add the new product to the session and commit to the database
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# Endpoint to read all products (GET /)


@router.get("/", response_model=list[Product])
async def read_products(session: Session = Depends(get_session)):
    # Fetch all products from the database
    products = session.exec(select(Product)).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found.")
    return products


# Endpoint to read a specific product by its ID (GET /{id})


@router.get("/{id}")
async def read_product(id: int, session: Session = Depends(get_session)):
    # Fetch the product by its ID
    product = session.exec(select(Product).where(Product.id == id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    return product


# Endpoint to update a product by its ID (PUT /{id})


@router.put("/{id}", dependencies=[Depends(admin_only)])
async def update_product(
    id: int,
    product: Product,
    session: Session = Depends(get_session),
):
    # Fetch the existing product from the database
    existing_product = session.exec(select(Product).where(Product.id == id)).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")

    # Update the product's details
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.stock = product.stock
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)
    return existing_product


# Endpoint to delete a product by its ID (DELETE /{id})


@router.delete("/{id}", dependencies=[Depends(admin_only)])
async def delete_product(id: int, session: Session = Depends(get_session)):
    # Fetch the product to delete
    product = session.exec(select(Product).where(Product.id == id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")

    # Delete the product and commit the change
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully."}
