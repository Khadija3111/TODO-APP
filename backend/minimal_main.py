from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="Todo API")

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

# Include minimal API functionality
@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API (minimal version)"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)