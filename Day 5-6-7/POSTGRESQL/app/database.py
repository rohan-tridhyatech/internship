from contextlib import asynccontextmanager
from sqlmodel import Session, SQLModel
from config import engine

# Create Function for Table Creation
def create_tables():
    SQLModel.metadata.create_all(engine)

# Create Function for Session Management
def get_session():
    with Session(engine) as session:
        yield session

# Create Context Manager for APP Lifespan
@asynccontextmanager
async def lifespan(app):
    print("Creating Tables............")
    create_tables()
    print("Create Table Successfully")
    yield