from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import text

from database import get_db
from models import Todo
from schemas import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoList

router = APIRouter(prefix="/todos", tags = ["Todos"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("Select 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "All system operational"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database Connection failed {str(e)}")
    
# CRUD Endpoints

@router.post("", response_model=ToDoResponse, status_code=201)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    try:
        db_todo = Todo(
            title = todo.title,
            description = todo.description,
            completed = todo.completed
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create todo: {str(e)}")
    
@router.get("/todos", response_model=ToDoList)
def get_tools(page: int = Query(1, ge=1, description = "Page Number"),
                per_page: int = Query(10, ge=1, description = "Items per page"),
                completed: Optional[bool] = Query(None, description="Filter by Completion Status"),
                search: Optional[str] = Query(None, description="Search in title and description"),
                db: Session = Depends(get_db)
                ):
    """
    Get a list of todos with pagination and filtering.
    
    - **page**: Page number (starts from 1)
    - **per_page**: Number of items per page (1-100)
    - **completed**: Filter by completion status (true/false)
    - **search**: Search text in title and description.
    """

    try:
        query = db.query(Todo)

        if completed is not None:
            query = query.filter(Todo.completed == completed)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Todo.title.ilike(search_term) | 
                Todo.description.ilike(search_term)
            )

        # Get total count before pagination.
        total = query.count()

        # Apply Pagination
        offset = (page - 1) * per_page
        todos = query.order_by(Todo.created_at.desc()).offset(offset).limit(per_page).all()

        return ToDoList(
            todos = todos,
            total = total,
            page = page, 
            per_page = per_page
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Failed to fetch todos: {str(e)}")
    
@router.get("todos/{todo_id}", response_model = ToDoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Get a specific todo by ID.
    
    - **todo_id**: Unique identifier of the todo
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    return todo

@router.put("/todos{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, todo_update: ToDoUpdate , db: Session = Depends(get_db)):
    """
    Update a specific todo.
    
    - **todo_id**: Unique identifier of the todo
    - Only provided fields will be updated
    """
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        
        # Update only provided fields
        update_data = todo_update.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(todo, field, value)

        db.commit()
        db.refresh(todo)
        return todo
    
# Use try...except HTTPException only when:
# You are catching other exceptions (e.g., SQLAlchemyError, ValueError) in a try block and want to let HTTPException pass through unchanged — so it still returns the correct HTTP response.
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update todo: {str(e)}")
    
@router.delete("todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try: 
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        
        db.delete(todo)
        db.commit()

        return {"message": f"Todo with id {todo_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete the todo: {str(e)}")
    

@router.patch("/todos/{todo_id}/toggle", response_model=ToDoResponse)
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Toggle the completion status of a todo.
    
    - **todo_id**: Unique identifier of the todo
    """
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
        
        todo.completed = not todo.completed

        db.commit()
        db.refresh(todo)

        return todo 
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle todo: {str(e)}")
    
# Statistics endpoint
@router.get("/todos/stats/summary")
def get_todo_stats(db: Session = Depends(get_db)):
    """Get summary statistics about todos."""

    try:
        total = db.query(Todo).count()
        completed = db.query(Todo).filter(Todo.completed == True).count()
        pending = total - completed
        
        return {
            "total_todos": total, 
            "completed_todos": completed,
            "pending_todos": pending,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Statistics: {str(e)}")
