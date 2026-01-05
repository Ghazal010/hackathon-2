from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import auth, tasks
from .database import engine
from .models import user, task  # Import models to create tables

# Create database tables
user.User.metadata.create_all(bind=engine)
task.Task.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Todo App API",
    description="API for the Todo App - Phase II: Full-Stack Web Application",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo App API - Phase II", "version": "2.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}