# Phase II Implementation: Full-Stack Web Application

## Overview
This document details the technical implementation approach for Phase II: Full-Stack Web Application. It captures the architecture decisions, technical challenges, and implementation details for converting the console application into a full-stack web application with user authentication and database persistence.

## Architecture Overview

### Frontend Architecture
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API or Zustand
- **API Client**: Custom service layer with fetch API
- **Authentication**: JWT-based authentication with secure cookie storage

### Backend Architecture
- **Framework**: FastAPI
- **Database**: SQLModel with Neon DB (PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **API Design**: RESTful endpoints following FastAPI best practices
- **Documentation**: Automatic API documentation via FastAPI

### Database Schema
- **Users Table**: Stores user authentication data
- **Tasks Table**: Stores task data with foreign key to users
- **Relationships**: One-to-many relationship between users and tasks
- **Indexing**: Proper indexing on frequently queried fields

## Technical Implementation Details

### 1. Frontend Implementation

#### Project Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── reset-password/
│   ├── dashboard/
│   │   ├── tasks/
│   │   │   ├── create/
│   │   │   ├── [id]/
│   │   │   └── [...filters]/
│   │   └── export/
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskItem.tsx
│   │   └── TaskFilters.tsx
│   └── ui/
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── LoadingSpinner.tsx
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   └── types.ts
└── package.json
```

#### Key Components Implementation

**Authentication Components:**
- `LoginForm.tsx`: Handles user login with validation
- `RegisterForm.tsx`: Handles user registration with password strength validation
- `ProtectedRoute.tsx`: Higher-order component to protect routes requiring authentication

**Task Management Components:**
- `TaskList.tsx`: Displays paginated list of tasks with filtering/sorting
- `TaskForm.tsx`: Handles task creation and editing with validation
- `TaskItem.tsx`: Individual task display with completion toggle

#### API Service Implementation
```typescript
// lib/api.ts
class ApiService {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    this.token = null;
  }

  setToken(token: string) {
    this.token = token;
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  // Authentication methods
  login(credentials: { email: string; password: string }) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  register(userData: { email: string; password: string; name: string }) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Task methods
  getTasks(filters?: { status?: string; priority?: string; search?: string }) {
    const queryString = new URLSearchParams(filters).toString();
    return this.request(`/api/tasks?${queryString}`);
  }

  createTask(taskData: { title: string; description?: string; priority?: string; dueDate?: string }) {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  updateTask(id: number, taskData: Partial<Task>) {
    return this.request(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  deleteTask(id: number) {
    return this.request(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  toggleTaskCompletion(id: number) {
    return this.request(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }

  exportTasks(format: 'pdf' | 'csv') {
    return this.request(`/api/tasks/export/${format}`, {
      method: 'GET',
    });
  }
}
```

### 2. Backend Implementation

#### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── password.py
│   │   └── validators.py
│   └── dependencies.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── requirements.txt
└── alembic.ini
```

#### Database Models Implementation

**User Model:**
```python
# models/user.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
```

**Task Model:**
```python
# models/task.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    due_date: Optional[datetime] = Field(default=None)

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
```

#### API Endpoints Implementation

**Authentication Endpoints:**
```python
# api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserRead
from app.database import get_session
from app.schemas.user import Token, TokenData
from app.utils.password import verify_password, get_password_hash
from app.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(email: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

**Task Endpoints:**
```python
# api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, and_
from typing import List, Optional
from datetime import datetime
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from app.models.user import User
from app.database import get_session
from app.dependencies import get_current_user

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
```

### 3. Security Implementation

#### Authentication Security
- Passwords hashed using bcrypt with proper salt
- JWT tokens with configurable expiration
- Secure token storage and transmission
- Rate limiting for authentication endpoints
- Input validation and sanitization

#### API Security
- All endpoints protected by authentication middleware
- Proper CORS configuration
- SQL injection prevention via SQLModel parameterization
- Input validation using Pydantic schemas

### 4. Export Functionality Implementation

#### PDF Export
```python
# utils/export.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

def generate_pdf_tasks(tasks):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("Task Export", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Create table data
    data = [['ID', 'Title', 'Description', 'Status', 'Priority', 'Due Date']]
    for task in tasks:
        data.append([
            str(task.id),
            task.title,
            task.description or '',
            'Completed' if task.completed else 'Pending',
            task.priority,
            task.due_date.strftime('%Y-%m-%d') if task.due_date else ''
        ])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(table)
    doc.build(story)

    buffer.seek(0)
    return buffer
```

#### CSV Export
```python
import csv
from io import StringIO

def generate_csv_tasks(tasks):
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['ID', 'Title', 'Description', 'Status', 'Priority', 'Due Date', 'Created At'])

    # Write task data
    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.description or '',
            'Completed' if task.completed else 'Pending',
            task.priority,
            task.due_date.strftime('%Y-%m-%d') if task.due_date else '',
            task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return output.getvalue()
```

## Implementation Challenges and Solutions

### Challenge 1: Data Migration from Phase I
- **Issue**: Converting in-memory data structure to database model
- **Solution**: Create migration path that preserves existing task structure while adding user relationships

### Challenge 2: Authentication Integration
- **Issue**: Adding user authentication to existing task management system
- **Solution**: Implement authentication middleware that protects task endpoints and ensures user isolation

### Challenge 3: Real-time Updates
- **Issue**: Providing real-time updates without WebSockets
- **Solution**: Implement polling with exponential backoff or Server-Sent Events for updates

### Challenge 4: Responsive Design
- **Issue**: Creating responsive UI that works on all device sizes
- **Solution**: Use Tailwind CSS utility classes with mobile-first approach

## Performance Considerations

### Database Performance
- Proper indexing on frequently queried fields (user_id, completed, priority)
- Pagination for large task lists
- Connection pooling for database operations

### Frontend Performance
- Code splitting for faster initial load
- Client-side caching for API responses
- Optimized image loading and compression

### API Performance
- Efficient query construction with SQLModel
- Rate limiting to prevent abuse
- Caching for frequently accessed data

## Testing Strategy

### Backend Testing
- Unit tests for individual functions and endpoints
- Integration tests for authentication flows
- Database transaction tests
- Security tests for authentication middleware

### Frontend Testing
- Component tests for UI elements
- Integration tests for API interactions
- End-to-end tests for user workflows
- Accessibility tests

## Deployment Considerations

### Environment Configuration
- Separate configuration for development, staging, and production
- Secure handling of environment variables
- Database connection configuration

### Security Configuration
- HTTPS enforcement
- Secure headers configuration
- Proper CORS policy
- Environment-specific security settings
