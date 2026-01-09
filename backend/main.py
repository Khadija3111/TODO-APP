import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import using relative paths since we're in the backend directory
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from utils.database import create_db_and_tables

app = FastAPI(title="Todo API")

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

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# This is the main entry point for the FastAPI application