from starlette.config import Config
from sqlmodel import create_engine

# Initialize Config
try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Fetch DATABASE_URL from config
DATABASE_URL = config("DATABASE_URL", cast=str)

# Adjust connection string for SQLAlchemy
conn_string: str = DATABASE_URL.replace("postgresql", "postgresql+psycopg2")

# Create Engine
engine = create_engine(conn_string, echo=True)
