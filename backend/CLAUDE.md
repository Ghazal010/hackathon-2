# Backend Guidelines - Phase I

## Stack
- Python 3.13+
- UV package manager
- Claude Code
- Spec-Kit Plus

## Project Structure
- `src/main.py` - Main console application
- `models.py` - Data models (if needed in later phases)
- `requirements.txt` - Dependencies

## Python Conventions
- Use type hints for all function parameters and return values
- Follow PEP 8 style guide
- Use descriptive variable and function names
- Include docstrings for classes and functions
- Handle errors gracefully with appropriate messages

## Running the Application
```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the console app
python src/main.py
```

## Phase I Specifics
- In-memory storage only (no database)
- Console-based user interface
- Implement all 5 Basic Level features:
  1. Add Task
  2. Delete Task
  3. Update Task
  4. View Task List
  5. Mark as Complete

## Spec-Driven Development
- All changes must be specified in markdown files before implementation
- Reference specifications: @specs/features/task-crud.md
- Update specs if requirements change during development