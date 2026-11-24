from ..settings import CONFIG
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def create_database_engine() -> Engine:
    url = (
        f"{CONFIG.DATABASE_DRIVER}://{CONFIG.DATABASE_USER}:{CONFIG.DATABASE_PASSWORD}@"
        f"{CONFIG.DATABASE_HOST}:{CONFIG.DATABASE_PORT}/{CONFIG.DATABASE_NAME}"
    )
    return create_engine(url)
