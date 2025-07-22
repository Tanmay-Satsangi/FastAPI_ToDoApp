"""
Database models using SQLAlchemy ORM.
These represent the structure of our database tables.
"""


"""
    Todo model represents a todo item in our database.

    Columns:
    - id: Primary key, auto-incrementing integer
    - title: Todo title (required, max 200 chars)
    - description: Optional longer description
    - completed: Boolean flag for completion status
    - created_at: Timestamp when todo was created
    - updated_at: Timestamp when todo was last updated
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Todo(Base):
   __tablename__ = "todos"

   id = Column(Integer, primary_key=True, index=True)
   title = Column(String(200), nullable=False, index=True)
   description = Column(Text, nullable=True)
   completed = Column(Boolean, default=False, index=True)
   # Timestamps - automatically managed by PostgreSQL
   created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(), 
                    nullable=False
                    )
   updated_at = Column(
                        DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now(),
                        nullable=False
                    )
