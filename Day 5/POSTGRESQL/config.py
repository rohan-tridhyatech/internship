from starlette.config import Config
from starlette.datastructures import Secret


# class Settings(BaseSettings):
#     DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/mydatabase"

#     class Config:
#         env_file = ".env"  # Load from .env file if present

# settings = Settings()


try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()    

DATABASE_URL = config("DATABASE_URL", cast=Secret)