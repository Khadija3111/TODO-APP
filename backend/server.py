import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import using absolute paths
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from utils.database import create_db_and_tables

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