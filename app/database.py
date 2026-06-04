from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Database engine
engine = create_engine(DATABASE_URL)

# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Creates and closes a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
