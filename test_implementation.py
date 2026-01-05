"""
Test script to verify Phase II implementation
This script checks that all the basic components of the backend are properly set up
"""

import sys
import os
from pathlib import Path

# Add the backend to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_backend_structure():
    """Test that backend structure is properly set up"""
    print("Testing backend structure...")

    # Check if required files exist
    backend_path = Path(__file__).parent / "backend"

    required_files = [
        "main.py",
        "config.py",
        "database.py",
        "models/user.py",
        "models/task.py",
        "api/auth.py",
        "api/tasks.py",
        "utils/password.py",
        "utils/auth.py",
        "dependencies.py",
        "requirements.txt"
    ]

    missing_files = []
    for file in required_files:
        file_path = backend_path / file
        if not file_path.exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing backend files: {missing_files}")
        return False
    else:
        print("✅ All backend files present")
        return True

def test_frontend_structure():
    """Test that frontend structure is properly set up"""
    print("Testing frontend structure...")

    # Check if required frontend files exist
    frontend_path = Path(__file__).parent / "frontend"

    required_files = [
        "package.json",
        "tsconfig.json",
        "tailwind.config.js",
        "next.config.js",
        "app/page.tsx",
        "app/layout.tsx",
        "app/login/page.tsx",
        "app/register/page.tsx",
        "app/dashboard/page.tsx",
        "lib/api.ts",
        "lib/types.ts",
        "app/globals.css"
    ]

    missing_files = []
    for file in required_files:
        file_path = frontend_path / file
        if not file_path.exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing frontend files: {missing_files}")
        return False
    else:
        print("✅ All frontend files present")
        return True

def test_imports():
    """Test that we can import backend modules without errors"""
    print("Testing backend imports...")

    try:
        # Test importing main modules
        from backend import main, config, database
        from backend.models import user, task
        from backend.api import auth, tasks
        from backend.utils import password, auth as auth_utils
        from backend import dependencies

        print("✅ All backend modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error during import: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Phase II Implementation Tests\n")

    tests = [
        test_backend_structure,
        test_frontend_structure,
        test_imports
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()  # Add a blank line between tests

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"Test Summary: {passed}/{total} test groups passed")

    if passed == total:
        print("🎉 All tests passed! Phase II implementation is ready.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)