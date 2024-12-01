# Entry point for the FastAPI application
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel


# ########################## Pydantic Models ##########################
# Base models for Category and Product used for validation and serialization
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

# ########################## Database Models ##########################
# SQLAlchemy ORM models for Category and Product

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")



# ########################## Database Setup ##########################
DATABASE_URL = "sqlite:///./products.db"

# Create engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
Base.metadata.create_all(bind=engine)

# ########################## CRUD Operations ##########################
# Operations for interacting with the database
def get_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product




## ########################## API Routes ##########################
# Routes for interacting with Categories and Products

router = APIRouter()

# Category Endpoints
@router.get("/categories", response_model=list[Category])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.post("/categories", response_model=Category)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)


# Product Endpoints
@router.get("/products", response_model=list[Product])
def read_products(db: Session = Depends(get_db)):
    return get_products(db)


@router.post("/products", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)


# ########################## Application Setup ##########################
app = FastAPI(title="Simple Project Management API")

# Include the API routes
app.include_router(router)