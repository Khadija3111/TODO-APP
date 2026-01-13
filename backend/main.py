import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the current directory to the path to resolve imports properly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import using relative paths
try:
    from api.auth import router as auth_router
    from api.tasks import router as tasks_router
    from utils.database import create_db_and_tables
except ImportError as e:
    print(f"Import error: {e}")
    # Try alternative import method
    import importlib.util
    auth_spec = importlib.util.spec_from_file_location("auth", "./api/auth.py")
    auth_module = importlib.util.module_from_spec(auth_spec)
    auth_spec.loader.exec_module(auth_module)
    auth_router = auth_module.router

    tasks_spec = importlib.util.spec_from_file_location("tasks", "./api/tasks.py")
    tasks_module = importlib.util.module_from_spec(tasks_spec)
    tasks_spec.loader.exec_module(tasks_module)
    tasks_router = tasks_module.router

    db_spec = importlib.util.spec_from_file_location("database", "./utils/database.py")
    db_module = importlib.util.module_from_spec(db_spec)
    db_spec.loader.exec_module(db_module)
    create_db_and_tables = db_module.create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Todo API",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app",  # Your Vercel deployment
        "https://todo-app-2.vercel.app",  # Main Vercel domain for your project
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(tasks_router, prefix="/api/tasks")

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API"}

# This is the main entry point for the FastAPI application
