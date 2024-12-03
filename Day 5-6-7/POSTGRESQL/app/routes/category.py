from __future__ import annotations

from app.auth import admin_only
from app.database import get_session
from app.models import Category
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel import Session

# Importing models, database session, and authentication utilities

router = APIRouter()

# Endpoint to create a new category (POST /)


@router.post("/", response_model=Category, dependencies=[Depends(admin_only)])
async def create_category(category: Category, session: Session = Depends(get_session)):
    # Check if a category with the same name already exists
    existing_category = session.exec(
        select(Category).where(Category.name == category.name),
    ).first()
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists.",
        )

    # Add the new category to the session and commit to the database
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


# Endpoint to read all categories (GET /)


@router.get("/", response_model=list[Category])
async def read_categories(session: Session = Depends(get_session)):
    # Fetch all categories from the database
    categories = session.exec(select(Category)).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found.")
    return categories


# Endpoint to read a specific category by its ID (GET /{id})


@router.get("/{id}")
async def read_category(id: int, session: Session = Depends(get_session)):
    # Fetch a category by its ID from the database
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with ID {id} not found.")
    return category


# Endpoint to update a category by its ID (PUT /{id})


@router.put("/{id}", dependencies=[Depends(admin_only)])
async def update_category(
    id: int,
    category: Category,
    session: Session = Depends(get_session),
):
    # Fetch the existing category from the database
    existing_category = session.exec(select(Category).where(Category.id == id)).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail=f"Category with ID {id} not found.")

    # Update the category's name
    existing_category.name = category.name
    session.add(existing_category)
    session.commit()
    session.refresh(existing_category)
    return existing_category


# Endpoint to delete a category by its ID (DELETE /{id})


@router.delete("/{id}", dependencies=[Depends(admin_only)])
async def delete_category(id: int, session: Session = Depends(get_session)):
    # Fetch the category to delete
    category = session.exec(select(Category).where(Category.id == id)).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with ID {id} not found.")

    # Delete the category and commit the change
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully."}
