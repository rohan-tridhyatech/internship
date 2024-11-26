from starlette.config import Config
from starlette.datastructures import Secret

config = Config()
try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()    

DATABASE_URL = config("DATABASE_URL", cast=Secret)