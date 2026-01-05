from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, and_
from typing import List, Optional
from datetime import datetime
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..models.user import User
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = Task(
        **task.dict(),
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    query = select(Task).where(Task.user_id == current_user.id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority:
        query = query.where(Task.priority == priority)

    if search:
        query = query.where(Task.title.contains(search) | Task.description.contains(search))

    tasks = session.exec(query).all()
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/complete")
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return {"completed": db_task.completed}