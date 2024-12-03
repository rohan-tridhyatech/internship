from __future__ import annotations

from contextlib import asynccontextmanager

from sqlmodel import Session
from sqlmodel import SQLModel

from .config import engine  # Import the database engine from the config module

# Function to create all tables defined in SQLModel


def create_tables():
    # This will create all tables in the database based on the SQLModel metadata
    SQLModel.metadata.create_all(engine)


# Function for session management, returning a session to interact with the database


def get_session():
    # This is a generator function that provides a session to interact with the database
    with Session(engine) as session:
        yield session  # Yield the session for use in queries


# Context manager for app lifespan to handle setup and teardown


@asynccontextmanager
async def lifespan(app):
    print("Creating Tables............")
    create_tables()  # Calls the create_tables function to create necessary tables
    print("Create Table Successfully")
    yield  # Yield control back to the application during its lifespan
