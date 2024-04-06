from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_USER = "nordic_peace"
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PASSWORD = "nordic_peace"
# POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_DB = "nordic_peace_db"
POSTGRES_HOST = "hacknarock_postgres"
POSTGRES_PORT = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_reset_on_return=None,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
