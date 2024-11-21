from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
import config
from typing import Annotated
from contextlib import asynccontextmanager


# Create a Model
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False, unique=True)
    
    # Relationship to the Product model
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, nullable=False)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int = Field(foreign_key="category.id")

    # Relationship to the Category model
    category: Category = Relationship(back_populates="products")


# Create Engine
conn_string: str = str(config.DATABASE_URL).replace("postgresql","postgresql+psycopg2")
engine = create_engine(conn_string, connect_args={"sslmode":"require"}, pool_recycle=300, pool_size=10, echo=True)

# Create Function for Table Creation
def create_tables():
    SQLModel.metadata.create_all(engine)

# Session : seprate session for each functionality/transaction
# Create Function for Session Management
def get_session():
    with Session(engine) as session:
        yield session

# Create Context Manager for APP Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables............")
    create_tables()
    print("Create Table Successfully")
    yield

app: FastAPI = FastAPI(lifespan=lifespan, title="Product Management App")

# Create Endpoints of APP
# *********************** CATEGOTY APIs ***********************

@app.post("/category", response_model=Category)
async def create_category(category: Category, session: Annotated[Session,Depends(get_session)]):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@app.get("/category", response_model=list[Category])
async def read_category(session: Annotated[Session,Depends(get_session)]):
    categories = session.exec(select(Category)).all()
    if categories:
        return categories
    else:
        raise HTTPException(status_code=404, detail="Categoty Not Found.")

@app.get("/category/{id}")
async def read_single_category(id: int, session: Annotated[Session,Depends(get_session)]):
    category = session.exec(select(Category).where(Category.id==id)).first()
    if category:
        return category
    else:
        raise HTTPException(status_code=404, detail= f"Categoty Not Found with Id: {id}.")
    

@app.put("/category/{id}")
async def update_category(id: int, category: Category, session: Annotated[Session,Depends(get_session)]):
    existing_category = session.exec(select(Category).where(Category.id==id)).first()
    if existing_category:
        existing_category.name = category.name
        session.add(existing_category)
        session.commit()
        session.refresh(existing_category)
        return existing_category
    else:
        raise HTTPException(status_code=404, detail="No Category Found.")

    
@app.delete("/category/{id}")
async def delete_category(id: int, session: Annotated[Session,Depends(get_session)]):
    category = session.exec(select(Category).where(Category.id==id)).first()
    if category:
        session.delete(category)
        session.commit()
        return {"message" : "Category Deleted Successfully."}
    else:
        raise HTTPException(status_code=404, detail="No Category Found.")
   


# *********************** PRODUCTS APIs ***********************
@app.post("/products", response_model=Product)
async def create_product(product: Product, session: Annotated[Session,Depends(get_session)]):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products", response_model=list[Product])
async def read_products(session: Annotated[Session,Depends(get_session)]):
    products = session.exec(select(Product)).all()
    if products:
        return products
    else:
        raise HTTPException(status_code=404, detail="Products Not Found.")


@app.get("/products/{id}")
async def read_single_product(id: int, session: Annotated[Session,Depends(get_session)]):
    product = session.exec(select(Product).where(Product.id==id)).first()
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail= f"Product Not Found with Id: {id}.")
    

@app.put("/products/{id}")
async def update_product(id: int, product: Product, session: Annotated[Session,Depends(get_session)]):
    existing_product = session.exec(select(Product).where(Product.id==id)).first()
    if existing_product:
        existing_product.name = product.name
        existing_product.price = product.price
        existing_product.stock = product.stock
        session.add(existing_product)
        session.commit()
        session.refresh(existing_product)
        return existing_product
    else:
        raise HTTPException(status_code=404, detail="Product No Found.")

    
@app.delete("/products/{id}")
async def delete_product(id: int, session: Annotated[Session,Depends(get_session)]):
    product = session.exec(select(Product).where(Product.id==id)).first()
    if product:
        session.delete(product)
        session.commit()
        return {"message" : "Product Successfully Deleted."}
    else:
        raise HTTPException(status_code=404, detail="Product Not Found.")
   

# *********************** PRODUCTS BY CATEGORY APIs ***********************   
@app.get("/category{id}/products")
async def read_products_by_category(id:int, session: Annotated[Session,Depends(get_session)] ):
    products = session.exec(select(Product).where(Product.category_id==id)).all()
    if products:
        return products
    else:
        raise HTTPException(status_code=404, detail="Products Not Founf with Category ID: {id}")
