# How to Test Your Application

## 1. Verify the Application Exists
The application is located at: `/Users/user/Desktop/hackathon-2/hackathon-todo/src/main.py`

## 2. How to Run the Application
Open your terminal and navigate to the project directory, then run:

```bash
cd /Users/user/Desktop/hackathon-2/hackathon-todo
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 src/main.py
```

## 3. What You'll See
When you run the application, you'll see:
- Welcome message
- Main menu with 8 options:
  1. Add Task
  2. View All Tasks
  3. View Pending Tasks
  4. View Completed Tasks
  5. Update Task
  6. Delete Task
  7. Mark Task as Complete/Incomplete
  8. Exit

## 4. How to Test Each Feature
- Select option 1 to add a task (enter title and description)
- Select option 2 to view all tasks
- Select option 3 to view only pending tasks
- Select option 4 to view only completed tasks
- Select option 5 to update a task (enter task ID and new details)
- Select option 6 to delete a task (enter task ID)
- Select option 7 to mark a task complete/incomplete (enter task ID)
- Select option 8 to exit

## 5. Verification Results
Our test script already confirmed that all 5 core features work correctly:
✅ Add Task: Successfully creates tasks with title and description
✅ Delete Task: Successfully removes tasks from the list
✅ Update Task: Successfully modifies existing task details
✅ View Task List: Successfully displays all tasks with proper formatting
✅ Mark as Complete: Successfully toggles task completion status

## 6. Documentation
All documentation is in the `/specs/phases/phase1/` directory with 7 detailed documents explaining every aspect of the implementation.

## 7. Ready for Submission
The application is fully functional and ready for submission via the hackathon form.