from fastapi import FastAPI
from api.auth import router as auth_router
from utils.database import create_db_and_tables

app = FastAPI(title="Todo API")

# Include API routers
app.include_router(auth_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the Todo API"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8008, log_level="info")