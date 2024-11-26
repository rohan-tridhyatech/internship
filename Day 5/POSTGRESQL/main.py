from fastapi import FastAPI, Depends, BackgroundTasks
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import EmailStr,SecretStr
import config

# Utility function for standardized JSON response
def json_response(status: str, data=None, message=None):
    return JSONResponse(
        content={
            "status": status,
            "data": data,
            "message": message,
        }
    )

# Models
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False, unique=True)
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, nullable=False)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    orders: list["Orders"] = Relationship(back_populates="product")

class Orders(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(nullable=False)
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(ge=0)
    product: Product = Relationship(back_populates="orders")

# Database connection
conn_string: str = str(config.DATABASE_URL).replace("postgresql", "postgresql+psycopg2")
engine = create_engine(conn_string, echo=True)

# Create tables
def create_tables():
    SQLModel.metadata.create_all(engine)

# Session management
def get_session():
    with Session(engine) as session:
        yield session

# App lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME="rohanmovaliya64@gmail.com",
    MAIL_PASSWORD=SecretStr("bwyd hbkk sdwn turs"),
    MAIL_FROM="rohanmovaliya64@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Background task for sending email
async def send_order_confirmation(email: str, order_id: int):
    html = f"<p>Thanks for placing an order. Your Order ID is {order_id}.</p>"
    message = MessageSchema(
        subject="Order Confirmation",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Order confirmation email sent to {email} for Order ID: {order_id}")
    return {"order_id": order_id}

# FastAPI app
app = FastAPI(lifespan=lifespan, title="Product Management App")

# *********************** CATEGORY APIs ***********************
@app.post("/category")
async def create_category(category: Category, session: Annotated[Session, Depends(get_session)]):
    try:
        session.add(category)
        session.commit()
        session.refresh(category)
        return json_response(status="success", data=category, message="Category created successfully.")
    except Exception as e:
        return json_response(status="error", message=f"Failed to create category. Error: {str(e)}")

@app.get("/category")
async def read_category(session: Annotated[Session, Depends(get_session)]):
    categories = session.exec(select(Category)).all()
    if categories:
        return json_response(status="success", data=categories, message="Categories retrieved successfully.")
    return json_response(status="error", message="No categories found.")

@app.get("/category/{id}")
async def read_single_category(id: int, session: Annotated[Session, Depends(get_session)]):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if category:
        return json_response(status="success", data=category, message="Category retrieved successfully.")
    return json_response(status="error", message=f"Category not found with ID: {id}.")

@app.put("/category/{id}")
async def update_category(id: int, category: Category, session: Annotated[Session, Depends(get_session)]):
    existing_category = session.exec(select(Category).where(Category.id == id)).first()
    if existing_category:
        existing_category.name = category.name
        session.add(existing_category)
        session.commit()
        session.refresh(existing_category)
        return json_response(status="success", data=existing_category, message="Category updated successfully.")
    return json_response(status="error", message="Category not found.")

@app.delete("/category/{id}")
async def delete_category(id: int, session: Annotated[Session, Depends(get_session)]):
    category = session.exec(select(Category).where(Category.id == id)).first()
    if category:
        session.delete(category)
        session.commit()
        return json_response(status="success", message="Category deleted successfully.")
    return json_response(status="error", message="Category not found.")

# *********************** PRODUCT APIs ***********************
@app.post("/products")
async def create_product(product: Product, session: Annotated[Session, Depends(get_session)]):
    try:
        session.add(product)
        session.commit()
        session.refresh(product)
        return json_response(status="success", data=product, message="Product created successfully.")
    except Exception as e:
        return json_response(status="error", message=f"Failed to create product. Error: {str(e)}")

@app.get("/products")
async def read_products(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(Product)).all()
    if products:
        return json_response(status="success", data=products, message="Products retrieved successfully.")
    return json_response(status="error", message="No products found.")

@app.get("/products/{id}")
async def read_single_product(id: int, session: Annotated[Session, Depends(get_session)]):
    product = session.exec(select(Product).where(Product.id == id)).first()
    if product:
        return json_response(status="success", data=product, message="Product retrieved successfully.")
    return json_response(status="error", message=f"Product not found with ID: {id}.")

@app.put("/products/{id}")
async def update_product(id: int, product: Product, session: Annotated[Session, Depends(get_session)]):
    existing_product = session.exec(select(Product).where(Product.id == id)).first()
    if existing_product:
        existing_product.name = product.name
        existing_product.price = product.price
        existing_product.stock = product.stock
        session.add(existing_product)
        session.commit()
        session.refresh(existing_product)
        return json_response(status="success", data=existing_product, message="Product updated successfully.")
    return json_response(status="error", message="Product not found.")

@app.delete("/products/{id}")
async def delete_product(id: int, session: Annotated[Session, Depends(get_session)]):
    product = session.exec(select(Product).where(Product.id == id)).first()
    if product:
        session.delete(product)
        session.commit()
        return json_response(status="success", message="Product deleted successfully.")
    return json_response(status="error", message="Product not found.")

# *********************** PLACE ORDER API ***********************
@app.post("/place-order/")
async def place_order(order: Orders, background_tasks: BackgroundTasks, session: Annotated[Session, Depends(get_session)]):
    try:
        product = session.exec(select(Product).where(Product.id == order.product_id)).first()
        if not product:
            return json_response(status="error", message="Product not found.")
        
        if product.stock < order.quantity:
            return json_response(status="error", message="Insufficient stock.")
        
        session.add(order)
        product.stock -= order.quantity
        session.add(product)
        session.commit()
        session.refresh(order)

        background_tasks.add_task(send_order_confirmation, order.email, order.id)
        return json_response(
            status="success",
            data={"order_id": order.id},
            message="Order placed successfully."
        )
    except Exception as e:
        return json_response(status="error", message=f"Failed to place order. Error: {str(e)}")
