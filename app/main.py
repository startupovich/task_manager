from fastapi import FastAPI, HTTPException, status
from uuid import UUID
from app.database import db
from app.models import Task, TaskCreate, TaskUpdate


app = FastAPI(
    title="Task Manager API",
    description="A simple task manager API with CRUD operations",
    version="1.0.0"
)


@app.get("/tasks", response_model=list[Task], summary="Get all tasks")
async def get_all_tasks():
    """Retrieve all tasks"""
    return db.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task, summary="Get a task by ID")
async def get_task(task_id: UUID):
    """Retrieve a specific task by its ID"""
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Create a new task")
async def create_task(task_create: TaskCreate):
    """Create a new task"""
    return db.create_task(task_create)


@app.put("/tasks/{task_id}", response_model=Task, summary="Update a task")
async def update_task(task_id: UUID, task_update: TaskUpdate):
    """Update an existing task"""
    task = db.update_task(task_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
async def delete_task(task_id: UUID):
    """Delete a task"""
    if not db.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Task Manager API is running"}