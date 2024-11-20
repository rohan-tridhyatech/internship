# Entry point for the FastAPI application
from fastapi import FastAPI
from endpoints import router
from database import Base, engine

# Initialize the app
app = FastAPI(title="Simple Project Management API")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the API routes
app.include_router(router)
