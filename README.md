# Todo App - Phase II: Full-Stack Web Application

This is the implementation of Phase II of the Todo App hackathon: a full-stack web application with user authentication and database persistence.

## 🎉 Phase II Complete - 200 Points Earned!

We have successfully completed Phase II of the Hackathon II with all requirements satisfied. This phase has earned us **200 points** (Total: 300/1000 points).

### 🏆 Key Achievements:
- ✅ Full-stack web application with Next.js frontend and FastAPI backend
- ✅ User authentication system with JWT tokens
- ✅ Database persistence with SQLModel and Neon DB
- ✅ Complete task management with CRUD operations
- ✅ Responsive UI working on all device sizes
- ✅ Complete systematic documentation (6-document approach)
- ✅ Ready for Phase III implementation

For details about the Phase II completion, see [PHASE_II_COMPLETE_SUMMARY.md](./PHASE_II_COMPLETE_SUMMARY.md)

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLModel with Neon DB (PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Language**: Python 3.13+

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **API Client**: Axios

## Setup Instructions

### 1. Prerequisites
- Python 3.13+
- Node.js (v18+)
- npm or yarn
- UV package manager (optional but recommended)

### 2. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp ../.env.example .env
```

4. Configure your environment variables in `.env`:
   - `DATABASE_URL`: Your Neon DB connection string
   - `SECRET_KEY`: A secure random string for JWT signing
   - `NEXT_PUBLIC_API_URL`: URL for your frontend to connect to the backend

### 3. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install frontend dependencies:
```bash
npm install
```

3. Copy the environment file:
```bash
cp ../.env.example .env.local
```

4. Update the environment variables in `.env.local` if needed.

### 4. Database Setup

1. Sign up for a free account at [Neon](https://neon.tech/)
2. Create a new project
3. Get your connection string and update the `DATABASE_URL` in your `.env` file
4. The database tables will be created automatically when you start the application

### 5. Running the Application

#### Backend
```bash
cd backend
uvicorn main:app --reload
```
The backend will run on `http://localhost:8000` by default.

#### Frontend
```bash
cd frontend
npm run dev
```
The frontend will run on `http://localhost:3000` by default.

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: Database connection string (e.g., postgresql://user:pass@localhost:5432/todo_db)
- `SECRET_KEY`: Secret key for JWT token signing (use a strong random string)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL (e.g., http://localhost:8000)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/logout` - Logout

### Tasks
- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion status

## Features

- User registration and authentication
- Task creation, reading, updating, and deletion
- Task prioritization (low, medium, high)
- Task completion toggling
- Task filtering (all, active, completed)
- Responsive UI design
- Secure JWT-based authentication
- Database persistence with user isolation

## Project Structure

```
hackathon-todo/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database configuration
│   ├── models/          # Database models
│   ├── api/             # API route definitions
│   ├── utils/           # Utility functions
│   └── dependencies.py  # FastAPI dependencies
├── frontend/             # Next.js frontend
│   ├── app/             # App Router pages
│   ├── components/      # React components
│   ├── lib/             # Utility functions and types
│   ├── public/          # Static assets
│   └── styles/          # Global styles
└── specs/                # Systematic documentation
    └── phases/
        └── phase2/      # Phase II documentation
```

## Systematic Documentation

This project follows the systematic documentation approach with 6 core documents for each phase:
1. Constitution - Project identity and constraints
2. Specification - Technical requirements
3. Plan - Implementation strategy
4. Tasks - Work breakdown
5. Implementation - Technical details
6. Overview - Phase summary

## Development Workflow

This project uses spec-driven development with Claude Code and Spec-Kit Plus as established in Phase I. All features were specified in markdown files before implementation.