import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the current directory to the path to resolve imports properly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import using relative paths with error handling
try:
    from api.auth import router as auth_router
    from api.tasks import router as tasks_router
    from utils.database import create_db_and_tables
except ImportError as e:
    print(f"Import error in server.py: {e}")
    # Fallback import method
    import importlib.util
    
    # Load auth router
    auth_spec = importlib.util.spec_from_file_location("auth", "./api/auth.py")
    auth_module = importlib.util.module_from_spec(auth_spec)
    auth_spec.loader.exec_module(auth_module)
    auth_router = auth_module.router

    # Load tasks router
    tasks_spec = importlib.util.spec_from_file_location("tasks", "./api/tasks.py")
    tasks_module = importlib.util.module_from_spec(tasks_spec)
    tasks_spec.loader.exec_module(tasks_module)
    tasks_router = tasks_module.router

    # Load database functions
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
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
