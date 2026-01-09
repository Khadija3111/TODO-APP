import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set up the Python path for backend modules
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Import and initialize the database tables directly
from backend.utils.database import engine
from backend.models.user import User
from backend.models.task import Task
from sqlmodel import SQLModel

# Create tables
print("Creating database tables...")
SQLModel.metadata.create_all(engine)

# Now test the registration
from backend.api.auth import register
from backend.models.user import UserCreate
from sqlmodel import Session

print("Testing registration...")
with Session(engine) as session:
    user_data = UserCreate(email='test4@example.com', password='testpass123')
    try:
        result = register(user_data, session)
        print(f"Registration successful: {result}")
        session.commit()
        print("User saved successfully!")
    except Exception as e:
        print(f"Error during registration: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()