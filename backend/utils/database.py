from sqlmodel import create_engine, Session, SQLModel, select
import os

# Get database URL from environment variable (Railway sets this automatically with PostgreSQL addon)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")  # Fallback to SQLite for local dev

# Handle Railway's PostgreSQL URL format (convert postgres:// to postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Function to initialize the database tables
def create_db_and_tables():
    # Import models here to ensure they're registered with SQLModel metadata
    # Using a try-except to handle potential duplicate registration issues
    try:
        from ..models.user import User  # noqa: F401
    except:
        pass
    try:
        from ..models.task import Task  # noqa: F401
    except:
        pass
    SQLModel.metadata.create_all(engine)