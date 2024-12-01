from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app import Category
from app import get_session

router = APIRouter()

@router.post("/", response_model=Category)
async def create_category(category: Category, session: Session = Depends(get_session)):
    existing_category = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists.")
    
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.get("/", response_model=list[Category])
async def read_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found.")
    return categories

@router.get("/{id}")
async def read_category(id: int, session: Session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with ID {id} not found.")
    return category

@router.put("/{id}")
async def update_category(id: int, category: Category, session: Session = Depends(get_session)):
    existing_category = session.exec(select(Category).where(Category.id == id)).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail=f"Category with ID {id} not found.")

    existing_category.name = category.name
    session.add(existing_category)
    session.commit()
    session.refresh(existing_category)
    return existing_category

@router.delete("/{id}")
async def delete_category(id: int, session: Session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with ID {id} not found.")
    
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully."}
