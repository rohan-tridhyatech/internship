from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app import Product
from app import get_session

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/", response_model=list[Product])
async def read_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found.")
    return products

@router.get("/{id}")
async def read_product(id: int, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    return product

@router.put("/{id}")
async def update_product(id: int, product: Product, session: Session = Depends(get_session)):
    existing_product = session.exec(select(Product).where(Product.id == id)).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.stock = product.stock
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)
    return existing_product

@router.delete("/{id}")
async def delete_product(id: int, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found.")
    
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully."}
