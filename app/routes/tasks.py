"""Task management routes"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional, List
from app.models import Task, TaskCreate, TaskUpdate, TaskListResponse, TaskStatus, User
from app.database import db
from app.dependencies import get_current_user, require_admin
from app.exceptions import NotFoundException, ForbiddenException

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    task = db.create_task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )
    
    return Task(**task)

@router.get("", response_model=TaskListResponse)
async def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    sort_by: str = Query("created_at", description="Sort field (prefix with - for ascending)"),
    current_user: User = Depends(get_current_user)
):
    """List tasks with pagination, filtering, and sorting"""
    tasks = db.get_user_tasks(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        sort_by=sort_by
    )
    
    total = db.count_user_tasks(current_user.id, status=status)
    
    task_models = [Task(**task) for task in tasks]
    
    return TaskListResponse(
        tasks=task_models,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific task"""
    task = db.get_task(task_id)
    
    if not task:
        raise NotFoundException(f"Task {task_id} not found")
    
    # Check ownership
    if task["user_id"] != current_user.id and current_user.role.value != "admin":
        raise ForbiddenException("You don't have access to this task")
    
    return Task(**task)

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a task"""
    task = db.get_task(task_id)
    
    if not task:
        raise NotFoundException(f"Task {task_id} not found")
    
    # Check ownership
    if task["user_id"] != current_user.id:
        raise ForbiddenException("You don't have access to this task")
    
    # Update task
    updated_task = db.update_task(
        task_id=task_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )
    
    return Task(**updated_task)

@router.patch("/{task_id}", response_model=Task)
async def partial_update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Partially update a task"""
    return await update_task(task_id, task_data, current_user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete a task"""
    task = db.get_task(task_id)
    
    if not task:
        raise NotFoundException(f"Task {task_id} not found")
    
    # Check ownership
    if task["user_id"] != current_user.id:
        raise ForbiddenException("You don't have access to this task")
    
    db.delete_task(task_id)
    
    return None

@router.get("/admin/all", response_model=List[Task])
async def get_all_tasks(current_user: User = Depends(require_admin)):
    """Get all tasks (admin only)"""
    tasks = db.get_all_tasks()
    return [Task(**task) for task in tasks]
