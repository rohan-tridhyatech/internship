from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False, unique=True)
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, nullable=False)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="products")
    orders: list["Orders"] = Relationship(back_populates="product")

class Orders(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(nullable=False)
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(ge=0)
    product: "Product" = Relationship(back_populates="orders")
