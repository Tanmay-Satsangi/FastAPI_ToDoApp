"""
Database configuration and connection setup.
This file handles our PostgreSQL connection using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
# The engine is the starting point for any SQLAlchemy application
engine = create_engine(
    DATABASE_URL,
    # These settings are good for PostgreSQL in development
    echo=True,  # Set to False in production (shows SQL queries in console)
    pool_pre_ping=True,  # Verifies connections before use
)

# Create SessionLocal class
# Each instance will be a database session
SessionLocal = sessionmaker(
    autocommit=False,  # We'll commit manually for better control
    autoflush=False,   # We'll flush manually
    bind=engine
)

# Create Base class for our models
# All our database models will inherit from this
Base = declarative_base()

def get_db():
    """
    Dependency function that provides database sessions.
    FastAPI will automatically handle opening and closing the session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all tables in the database.
    This will be called when we start the application.
    """
    Base.metadata.create_all(bind=engine)

# Test database connection
def test_connection():
    """Test if we can connect to the database."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
