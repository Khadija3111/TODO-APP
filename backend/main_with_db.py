from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Direct imports - temporarily including chat router to test
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from api.chat import router as chat_router  # Including chat router
from utils.database import create_db_and_tables

# Initialize the database when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    try:
        create_db_and_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # Continue anyway to allow the server to start
    yield
    # Cleanup on shutdown if needed

app = FastAPI(
    title="Todo API",
    lifespan=lifespan  # Enable lifespan to initialize database
)

# Custom middleware to handle HTTPS properly behind reverse proxies like Railway
class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Check if the request came through HTTPS via headers set by Railway/Cloudflare
        if (request.headers.get('x-forwarded-proto') == 'https' or
            request.headers.get('x-forwarded-scheme') == 'https'):
            # Update the request URL to reflect HTTPS
            request.scope['scheme'] = 'https'

        response = await call_next(request)
        return response

# Add the HTTPS redirect middleware
app.add_middleware(HTTPSRedirectMiddleware)

# Add trusted host middleware for proper HTTPS handling behind proxies
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Adjust this in production for security
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app",  # Your Vercel deployment
        "https://todo-app-2.vercel.app",  # Main Vercel domain for your project
        "https://todo-app-2-n4bn0oin0-khadija3111s-projects.vercel.app",  # Another Vercel deployment variant
        "http://localhost:3000",  # Local frontend development
        "http://localhost:3001",  # Alternative local frontend port
        "http://localhost:3002",  # Another alternative local frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers - including chat router
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(chat_router)  # Including chat router without prefix to match frontend expectations

# Custom middleware to ensure CORS headers are added to all responses, including errors
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = None
    try:
        response = await call_next(request)
    except Exception as e:
        # Handle exceptions and create a response that includes CORS headers
        from fastapi.responses import JSONResponse
        import traceback
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    # Add CORS headers to all responses, including error responses
    # Allow the origin that made the request
    origin = request.headers.get("origin")
    if origin and any(allowed_origin in origin for allowed_origin in [
        "https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app",
        "https://todo-app-2.vercel.app",
        "https://todo-app-2-n4bn0oin0-khadija3111s-projects.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002"
    ]):
        response.headers.setdefault("Access-Control-Allow-Origin", origin)
    else:
        # Default to allowing localhost for development
        if origin and "localhost" in origin:
            response.headers.setdefault("Access-Control-Allow-Origin", origin)
        else:
            # Default to the first allowed origin if the request origin isn't recognized
            response.headers.setdefault("Access-Control-Allow-Origin", "http://localhost:3001")
    response.headers.setdefault("Access-Control-Allow-Credentials", "true")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.setdefault("Access-Control-Allow-Headers", "Authorization, Content-Type, X-Requested-With")
    return response

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API"}

# This is the main entry point for the FastAPI application