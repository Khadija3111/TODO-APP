from sqlmodel import create_engine, Session, SQLModel, select
import os

# Using Neon PostgreSQL database
NEON_DATABASE_URL = "postgresql://neondb_owner:npg_jftmSdl7g1Ze@ep-empty-brook-a7tg1x3v-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# In a real application, you would use environment variables for the database URL
DATABASE_URL = os.getenv("DATABASE_URL", NEON_DATABASE_URL)

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