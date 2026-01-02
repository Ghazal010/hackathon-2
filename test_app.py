#!/usr/bin/env python3
"""
Test script for Todo Console Application
This script tests all the basic functionality without requiring user input
"""

from src.main import TodoApp

def test_todo_app():
    print("Testing Todo Console Application...")

    # Create app instance
    app = TodoApp()

    # Test 1: Add tasks
    print("\n1. Testing Add Task functionality:")
    task1 = app.add_task("Buy groceries", "Milk, eggs, bread")
    task2 = app.add_task("Complete Hackathon Phase I", "Implement console app")

    # Test 2: List all tasks
    print("\n2. Testing View All Tasks:")
    app.list_tasks()

    # Test 3: Update task
    print("\n3. Testing Update Task:")
    app.update_task(1, "Buy groceries and fruits", "Milk, eggs, bread, apples")

    # Test 4: Mark task as complete
    print("\n4. Testing Mark as Complete:")
    app.toggle_task_completion(1)

    # Test 5: List pending tasks
    print("\n5. Testing View Pending Tasks:")
    app.list_tasks(show_completed=False)

    # Test 6: List completed tasks
    print("\n6. Testing View Completed Tasks:")
    app.list_tasks(show_completed=True)

    # Test 7: Delete task
    print("\n7. Testing Delete Task:")
    app.delete_task(2)

    # Test 8: Final list
    print("\n8. Final task list:")
    app.list_tasks()

    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_todo_app()