#!/usr/bin/env python3
"""
Script to start the backend server for the Todo App
"""
import subprocess
import sys
import os

def start_backend():
    """Start the FastAPI backend server"""
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")

    # Change to backend directory
    os.chdir(backend_dir)

    # Start the uvicorn server
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--reload",
        "--port", "8000"
    ]

    print("Starting backend server on http://localhost:8000")
    print("Press Ctrl+C to stop the server")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    start_backend()