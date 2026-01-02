#!/usr/bin/env python3
"""
Todo Console Application - Phase I
In-Memory Python Console App for Hackathon II

Implements all 5 Basic Level features:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark as Complete
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class Task:
    """Represents a single todo task"""

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title} - {self.description}"


class TodoApp:
    """Main Todo Application class with in-memory storage"""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the todo list"""
        if not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(self.next_id, title.strip(), description.strip())
        self.tasks[self.next_id] = task
        self.next_id += 1
        print(f"✓ Task added: {task.title}")
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        if task_id in self.tasks:
            deleted_task = self.tasks.pop(task_id)
            print(f"✓ Task deleted: {deleted_task.title}")
            return True
        else:
            print(f"✗ Task with ID {task_id} not found")
            return False

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Update an existing task"""
        if task_id not in self.tasks:
            print(f"✗ Task with ID {task_id} not found")
            return False

        task = self.tasks[task_id]
        updated = False

        if title is not None:
            new_title = title.strip()
            if new_title:
                task.title = new_title
                updated = True
            else:
                print("✗ Task title cannot be empty")
                return False

        if description is not None:
            task.description = description.strip()
            updated = True

        if updated:
            task.updated_at = datetime.now()
            print(f"✓ Task updated: {task.title}")

        return updated

    def toggle_task_completion(self, task_id: int) -> bool:
        """Toggle the completion status of a task"""
        if task_id not in self.tasks:
            print(f"✗ Task with ID {task_id} not found")
            return False

        task = self.tasks[task_id]
        task.completed = not task.completed
        task.updated_at = datetime.now()

        status = "completed" if task.completed else "marked as incomplete"
        print(f"✓ Task {status}: {task.title}")
        return True

    def list_tasks(self, show_completed: Optional[bool] = None) -> List[Task]:
        """List all tasks, optionally filtered by completion status"""
        tasks = list(self.tasks.values())

        if show_completed is not None:
            tasks = [task for task in tasks if task.completed == show_completed]

        if not tasks:
            print("No tasks found.")
        else:
            print(f"\n{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
            print("-" * 70)
            for task in sorted(tasks, key=lambda t: t.id):
                status = "✓ Done" if task.completed else "○ Pending"
                title = task.title[:27] + "..." if len(task.title) > 30 else task.title
                desc = task.description[:30] + "..." if len(task.description) > 30 else task.description
                print(f"{task.id:<4} {status:<8} {title:<30} {desc}")

        return tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID"""
        return self.tasks.get(task_id)


def print_menu():
    """Print the application menu"""
    print("\n" + "="*50)
    print("TODO CONSOLE APPLICATION")
    print("="*50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Update Task")
    print("6. Delete Task")
    print("7. Mark Task as Complete/Incomplete")
    print("8. Exit")
    print("-"*50)


def get_user_input(prompt: str) -> str:
    """Get input from user with a prompt"""
    return input(prompt).strip()


def main():
    """Main application loop"""
    app = TodoApp()
    print("Welcome to the Todo Console Application!")
    print("This is Phase I of Hackathon II - In-Memory Python Console App")

    while True:
        print_menu()
        choice = get_user_input("Select an option (1-8): ")

        try:
            if choice == "1":
                # Add Task
                title = get_user_input("Enter task title: ")
                if not title:
                    print("Task title cannot be empty!")
                    continue
                description = get_user_input("Enter task description (optional): ")
                app.add_task(title, description)

            elif choice == "2":
                # View All Tasks
                print("\nAll Tasks:")
                app.list_tasks()

            elif choice == "3":
                # View Pending Tasks
                print("\nPending Tasks:")
                app.list_tasks(show_completed=False)

            elif choice == "4":
                # View Completed Tasks
                print("\nCompleted Tasks:")
                app.list_tasks(show_completed=True)

            elif choice == "5":
                # Update Task
                try:
                    task_id = int(get_user_input("Enter task ID to update: "))
                    task = app.get_task(task_id)
                    if task:
                        print(f"Current: {task}")
                        new_title = get_user_input(f"Enter new title (current: '{task.title}', press Enter to keep): ")
                        new_desc = get_user_input(f"Enter new description (current: '{task.description}', press Enter to keep): ")

                        # Only update if user provided new values
                        title_update = new_title if new_title else None
                        desc_update = new_desc if new_desc else None
                        app.update_task(task_id, title_update, desc_update)
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Please enter a valid task ID (number).")

            elif choice == "6":
                # Delete Task
                try:
                    task_id = int(get_user_input("Enter task ID to delete: "))
                    app.delete_task(task_id)
                except ValueError:
                    print("Please enter a valid task ID (number).")

            elif choice == "7":
                # Mark Task as Complete/Incomplete
                try:
                    task_id = int(get_user_input("Enter task ID to toggle completion: "))
                    app.toggle_task_completion(task_id)
                except ValueError:
                    print("Please enter a valid task ID (number).")

            elif choice == "8":
                # Exit
                print("Thank you for using the Todo Console Application!")
                break

            else:
                print("Invalid option. Please select 1-8.")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()