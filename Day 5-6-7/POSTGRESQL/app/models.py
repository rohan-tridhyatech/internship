from __future__ import annotations

from pydantic import EmailStr  # Import EmailStr for email validation
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

# Category model to represent product categories


class Category(SQLModel, table=True):
    # Define the primary key and set index for performance
    id: int = Field(default=None, primary_key=True, index=True)
    # Name of the category with a max length of 100 characters and unique constraint
    name: str = Field(max_length=100, nullable=False, unique=True)
    # Define a relationship with Product (one-to-many)
    products: list[Product] = Relationship(back_populates="category")


# Product model to represent products within a category


class Product(SQLModel, table=True):
    # Define the primary key and set index for performance
    id: int = Field(default=None, primary_key=True, index=True)
    # Product name with a max length of 30 characters, and it's a required field
    name: str = Field(max_length=30, nullable=False)
    # Price of the product (greater than 0)
    price: float = Field(gt=0)
    # Stock quantity (greater than or equal to 0)
    stock: int = Field(ge=0)
    # Foreign key to link the product to a category
    category_id: int = Field(foreign_key="category.id")
    # Relationship to Category (many-to-one)
    category: Category = Relationship(back_populates="products")
    # Relationship to Orders (one-to-many)
    orders: list[Orders] = Relationship(back_populates="product")


# Orders model to represent customer orders for products


class Orders(SQLModel, table=True):
    # Define the primary key and set index for performance
    id: int = Field(default=None, primary_key=True, index=True)
    # Customer email (validated as a proper email format)
    email: EmailStr = Field(nullable=False)
    # Foreign key to link the order to a product
    product_id: int = Field(foreign_key="product.id")
    # Quantity of product ordered (greater than or equal to 0)
    quantity: int = Field(ge=0)
    # Relationship to Product (many-to-one)
    product: Product = Relationship(back_populates="orders")


# Users model to represent users in the system (for authentication and roles)


class Users(SQLModel, table=True):
    # Define the primary key and set index for performance
    id: int = Field(default=None, primary_key=True, index=True)
    # Username of the user, unique and required
    username: str = Field(unique=True, index=True, nullable=False)
    # Password for the user (required)
    password: str = Field(nullable=False)
    # Role of the user (e.g., "admin", "user", etc.)
    role: str = Field(nullable=False)
