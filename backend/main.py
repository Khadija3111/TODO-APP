from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Direct imports
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
    allow_origins=[
        "https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app",  # Your Vercel deployment
        "https://todo-app-2.vercel.app",  # Main Vercel domain for your project

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

# Custom middleware to ensure CORS headers are added to all responses, including errors
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    # Add CORS headers to all responses, including error responses
    # Allow the origin that made the request
    origin = request.headers.get("origin")
    if origin and any(allowed_origin in origin for allowed_origin in [
        "https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app",
        "https://todo-app-2.vercel.app",
  
    ]):
        response.headers.setdefault("Access-Control-Allow-Origin", origin)
    else:
        # Default to the first allowed origin if the request origin isn't recognized
        response.headers.setdefault("Access-Control-Allow-Origin", "https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app")
    response.headers.setdefault("Access-Control-Allow-Credentials", "true")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.setdefault("Access-Control-Allow-Headers", "Authorization, Content-Type, X-Requested-With")
    return response

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API"}

# This is the main entry point for the FastAPI application
