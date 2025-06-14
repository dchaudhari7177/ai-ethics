import subprocess
import sys
import os
import webbrowser
from time import sleep

def run_backend():
    """Run the FastAPI backend server."""
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--reload"],
        cwd=os.getcwd()
    )
    return backend_process

def run_frontend():
    """Run the React frontend development server."""
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "start"],
        cwd=os.path.join(os.getcwd(), "frontend")
    )
    return frontend_process

def main():
    try:
        # Start backend
        backend_process = run_backend()
        sleep(2)  # Wait for backend to start

        # Start frontend
        frontend_process = run_frontend()
        sleep(2)  # Wait for frontend to start

        # Open browser
        webbrowser.open("http://localhost:3000")

        # Keep the script running
        while True:
            sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main() 