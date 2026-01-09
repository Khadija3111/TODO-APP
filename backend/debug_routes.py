from fastapi import FastAPI
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from utils.database import create_db_and_tables

app = FastAPI(title="Todo API")

# Include API routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

# Print registered routes
print("Registered routes:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"  {route.methods} {route.path}")

print("\nTesting if auth routes are accessible...")
print("Expected registration endpoint: POST /api/auth/register")
print("Expected login endpoint: POST /api/auth/login")
print("Expected get user endpoint: GET /api/auth/me")