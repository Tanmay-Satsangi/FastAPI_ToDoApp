"""
FastAPI Todo Application with PostgreSQL.
This is a beginner-friendly todo app demonstrating CRUD operations.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
import os

from database import create_tables, test_connection
from endpoints import router

load_dotenv()

app = FastAPI(
    title = "Welcome to ToDoApp !!!", 
    description="A beginner-friendly todo application using FastAPI and PostgreSQL",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the FastAPI ToDo app", 
        "status": "healthy",
        "docs": "/docs"
    }

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host = "0.0.0.0", 
        port = 8000
    )
