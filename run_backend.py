import sys
import os

# Add the current directory to the Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now try to run the backend
if __name__ == "__main__":
    import uvicorn
    from backend.main import app

    print("Starting backend server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)