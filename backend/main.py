from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging

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
        "https://todo-app-2-n4bn0oin0-khadija3111s-projects.vercel.app"
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
