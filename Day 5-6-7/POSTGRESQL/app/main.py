from __future__ import annotations

from app.database import lifespan
from app.middleware import LoggingMiddleware
from app.routes import authentication
from app.routes import category
from app.routes import orders
from app.routes import product
from fastapi import FastAPI

# Import lifespan context manager for app startup/shutdown
# Import custom middleware for logging

# Initialize FastAPI application with custom lifespan (to handle table creation) and app title
app = FastAPI(lifespan=lifespan, title="Product Management App")

# Add custom middleware for logging to track requests and responses
app.add_middleware(LoggingMiddleware)

# Include routers for different app modules with appropriate prefixes and tags
# These routers will handle requests to different parts of the app: category, product, orders, authentication
# Routes for Category-related operations
app.include_router(category.router, prefix="/category", tags=["Category"])
# Routes for Product-related operations
app.include_router(product.router, prefix="/product", tags=["Product"])
# Routes for Order-related operations
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
# Routes for Authentication (login, register)
app.include_router(authentication.router)
