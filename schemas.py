# Pydantic Schemas

"""
Pydantic schemas for request/response validation.
These define the structure of data coming in and going out of our API.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ToDoBase(BaseModel):
    """Base schema with common todo fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, description="Optional todo description")
    completed: bool = Field(False, description="Completion status")

class ToDoCreate(ToDoBase):
    """
    Schema for creating a new todo.
    Inherits all fields from TodoBase.
    """
    pass 

class ToDoUpdate(BaseModel):
    """
    Schema for updating an existing todo.
    All fields are optional for partial updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[str] = None

class ToDoResponse(ToDoBase):
    """
    Schema for returning todo data to clients.
    Includes all fields plus id and timestamps.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    # Configure Pydantic to work with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

class ToDoList(BaseModel):
    """Schema for returning a list of todos with metadata."""
    todos: list[ToDoResponse]
    # pagination
    total: int
    page: int
    per_page: int
